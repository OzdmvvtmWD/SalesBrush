import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',)))
from utils.utils import save_division 

def test_regular_division():
    assert save_division(10, 2) == 5.0
    assert save_division(7, 2) == 3.5  


def test_custom_rounding():
    assert save_division(7, 3, round_result=2) == 2.33
    assert save_division(1, 3, round_result=3) == 0.333
    assert save_division(12, 3.0, round_result=3) == 4.0


def test_division_by_zero():
    assert save_division(5, 0) is None
    assert save_division(14, 0) is None


def test_negative_numbers():
    assert save_division(-10, 2) == -5.0
    assert save_division(10, -2) == -5.0
    assert save_division(-10, -2) == 5.0


def test_zero_numerator():
    assert save_division(0, 5) == 0.0
    assert save_division(0, -5) == 0.0
