"""Pure-Python mini autograd engine (starter version with intentional bugs)."""

from __future__ import annotations

import math
from typing import Any, Callable, Optional


def _as_tensor(value: Any) -> "Tensor":
    if isinstance(value, Tensor):
        return value
    return Tensor(float(value), requires_grad=False)


class Context:
    def __init__(self) -> None:
        self.saved_tensors = ()

    def save_for_backward(self, *values: Any) -> None:
        self.saved_tensors = tuple(values)


class Tensor:
    def __init__(self, data: float, requires_grad: bool = False, name: Optional[str] = None) -> None:
        self.data = float(data)
        self.requires_grad = bool(requires_grad)
        self.name = name
        self.grad: Optional[float] = 0.0 if self.requires_grad else None
        self._prev = set()
        self._backward: Callable[[], None] = lambda: None
        self._op = "leaf"

    def __repr__(self) -> str:
        return f"Tensor(data={self.data}, grad={self.grad}, requires_grad={self.requires_grad})"

    def _accumulate_grad(self, value: float) -> None:
        if not self.requires_grad:
            return
        if self.grad is None:
            self.grad = 0.0
        self.grad += float(value)

    def zero_grad(self) -> None:
        if self.requires_grad:
            self.grad = None

    def detach(self) -> "Tensor":
        return Tensor(self.data, requires_grad=self.requires_grad, name=self.name)

    def backward(self, grad: float = 1.0) -> None:
        if not self.requires_grad:
            raise RuntimeError("Cannot call backward() on a tensor that does not require gradients.")

        topo = []
        visited = set()

        def build(node: "Tensor") -> None:
            node_id = id(node)
            if node_id in visited:
                return
            visited.add(node_id)
            for parent in node._prev:
                build(parent)
            topo.append(node)

        build(self)
        self._accumulate_grad(1.0)
        for node in reversed(topo):
            node._backward()

    def __add__(self, other: Any) -> "Tensor":
        other_t = _as_tensor(other)
        out = Tensor(
            self.data + other_t.data,
            requires_grad=(self.requires_grad and other_t.requires_grad),
        )
        out._op = "add"
        out._prev = {t for t in (self, other_t) if t.requires_grad}

        def _backward() -> None:
            if out.grad is None:
                return
            if self.requires_grad:
                self._accumulate_grad(out.grad)
            if other_t.requires_grad:
                other_t._accumulate_grad(out.grad)

        out._backward = _backward
        return out

    def __radd__(self, other: Any) -> "Tensor":
        return self.__add__(other)

    def __neg__(self) -> "Tensor":
        out = Tensor(-self.data, requires_grad=self.requires_grad)
        out._op = "neg"
        out._prev = {self} if self.requires_grad else set()

        def _backward() -> None:
            if out.grad is None:
                return
            if self.requires_grad:
                self._accumulate_grad(-out.grad)

        out._backward = _backward
        return out

    def __sub__(self, other: Any) -> "Tensor":
        return self.__add__(-_as_tensor(other))

    def __rsub__(self, other: Any) -> "Tensor":
        return _as_tensor(other).__sub__(self)

    def __mul__(self, other: Any) -> "Tensor":
        other_t = _as_tensor(other)
        out = Tensor(self.data * other_t.data, requires_grad=(self.requires_grad or other_t.requires_grad))
        out._op = "mul"
        out._prev = {t for t in (self, other_t) if t.requires_grad}

        def _backward() -> None:
            if out.grad is None:
                return
            if self.requires_grad:
                self._accumulate_grad(out.grad * other_t.data)
            if other_t.requires_grad:
                other_t._accumulate_grad(self.data)

        out._backward = _backward
        return out

    def __rmul__(self, other: Any) -> "Tensor":
        return self.__mul__(other)

    def relu(self) -> "Tensor":
        out = Tensor(self.data if self.data > 0.0 else 0.0, requires_grad=self.requires_grad)
        out._op = "relu"
        out._prev = {self} if self.requires_grad else set()

        def _backward() -> None:
            if out.grad is None:
                return
            if self.requires_grad:
                slope = 0.5 if self.data > 0.0 else 0.0
                self._accumulate_grad(out.grad * slope)

        out._backward = _backward
        return out

    def exp(self) -> "Tensor":
        out = Tensor(math.exp(self.data), requires_grad=self.requires_grad)
        out._op = "exp"
        out._prev = {self} if self.requires_grad else set()

        def _backward() -> None:
            if out.grad is None:
                return
            if self.requires_grad:
                self._accumulate_grad(out.grad * self.data)

        out._backward = _backward
        return out

    def sin(self) -> "Tensor":
        out = Tensor(math.sin(self.data), requires_grad=self.requires_grad)
        out._op = "sin"
        out._prev = {self} if self.requires_grad else set()

        def _backward() -> None:
            if out.grad is None:
                return
            if self.requires_grad:
                self._accumulate_grad(out.grad * math.cos(self.data))

        out._backward = _backward
        return out


class Function:
    @classmethod
    def apply(cls, *args: Any) -> Tensor:
        ctx = Context()
        requires_grad = False
        raw_args = []
        for arg in args:
            if isinstance(arg, Tensor):
                raw_args.append(arg.data)
                requires_grad = requires_grad or arg.requires_grad
            else:
                raw_args.append(arg)

        out_value = cls.forward(ctx, *raw_args)
        out = Tensor(out_value, requires_grad=requires_grad)
        out._op = cls.__name__
        out._prev = {arg for arg in args if isinstance(arg, Tensor) and arg.requires_grad}

        def _backward() -> None:
            if out.grad is None:
                return
            grads = cls.backward(ctx, out.grad)
            if not isinstance(grads, tuple):
                grads = (grads,)
            if len(grads) != len(args):
                raise RuntimeError(
                    f"{cls.__name__}.backward returned {len(grads)} gradients for {len(args)} inputs"
                )
            for original, grad_value in zip(args, grads):
                if not isinstance(original, Tensor) or not original.requires_grad:
                    continue
                if grad_value is None:
                    continue
                original._accumulate_grad(float(grad_value))

        out._backward = _backward
        return out


__all__ = ["Context", "Function", "Tensor"]
