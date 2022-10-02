import pytest
from quantum import *
import numpy as np


def unique_circuit(arr):
    return arr == int("0001", 2)


def test_unique_sat_solver():
    qs = unique_sat_solver(unique_circuit, 4, 1)
    assert qs.get_amplitudes()[1] == 2.75
