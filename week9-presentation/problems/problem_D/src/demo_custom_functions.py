"""Custom autograd-style functions for ProblemD (starter version with intentional bugs)."""

from __future__ import annotations

from .mini_autograd import Function, Tensor


class Square(Function):
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)
        return x * x

    @staticmethod
    def backward(ctx, grad_out):
        (x,) = ctx.saved_tensors
        return (2.0 * x * grad_out,)


class Axpy(Function):
    @staticmethod
    def forward(ctx, a, x, y):
        ctx.save_for_backward(a, x)
        return a * x + y

    @staticmethod
    def backward(ctx, grad_out):
        a, x = ctx.saved_tensors
        grad_a = grad_out * x
        grad_x = grad_out * a
        grad_y = grad_out
        return grad_x, grad_a, grad_y


class Clamp01(Function):
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)
        if x < 0.0:
            return 0.0
        if x > 1.0:
            return 1.0
        return x

    @staticmethod
    def backward(ctx, grad_out):
        (x,) = ctx.saved_tensors
        if 0.0 < x < 1.0:
            return (0.0,)
        return (grad_out,)


class MulAdd(Function):
    @staticmethod
    def forward(ctx, x, y, z):
        ctx.save_for_backward(x, y)
        return x * y + z

    @staticmethod
    def backward(ctx, grad_out):
        x, y = ctx.saved_tensors
        return (grad_out * y, grad_out * x, grad_out)


def square(x: Tensor) -> Tensor:
    return Square.apply(x)


def axpy(a: Tensor, x: Tensor, y: Tensor) -> Tensor:
    return Axpy.apply(a, x, y)


def clamp01(x: Tensor) -> Tensor:
    return Clamp01.apply(x)


def mul_add(x: Tensor, y: Tensor, z: Tensor) -> Tensor:
    return MulAdd.apply(x, y, z)


__all__ = [
    "Square",
    "Axpy",
    "Clamp01",
    "MulAdd",
    "square",
    "axpy",
    "clamp01",
    "mul_add",
]

