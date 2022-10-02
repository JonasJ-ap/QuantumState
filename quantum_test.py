import pytest
import quantum
import numpy as np


def unique_circuit(bits):
    return bits == int("0001", 2)


def test_unique_sat_solver():
    qs = quantum.unique_sat_solver(unique_circuit, 4, 1)
    assert qs.get_amplitudes()[1] == 2.75
