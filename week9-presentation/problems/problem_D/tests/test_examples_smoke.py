from ProblemD.student.src.demo_custom_functions import square
from ProblemD.student.src.mini_autograd import Tensor


def test_smoke_forward_expression():
    x = Tensor(2.0, requires_grad=True)
    y = (x + 3.0) * 2.0
    assert y.data == 10.0


def test_smoke_custom_square_backward():
    x = Tensor(3.0, requires_grad=True)
    y = square(x)
    y.backward()
    assert y.data == 9.0
    assert x.grad is not None

