import math
import pytest
import sys
import os

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from src.master import Master


@pytest.fixture
def master_node():
    return Master()


@pytest.mark.parametrize("n", [0, 1, 5, 10, 500, 1000, 50000, 100000])
def test_factorial(master_node: Master, n: int) -> None:
    expected = math.factorial(n)
    actual = master_node.calc_factorial(n)
    assert (
        actual == expected
    ), f"Mismatch for {n}!: Expected: {expected}, but got {actual}"
