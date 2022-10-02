import pytest
from quantum import QuantumState
import quantum
import numpy as np

amplitudes = "[0.12,0,0,1]"


def unique_circuit(bits):
    return bits == int("0001", 2)


def test_init_default():
    qs = QuantumState(2)
    assert qs.get_amplitudes().all() == np.array([1, 0, 0, 0]).all()


def test_init_state():
    qs = QuantumState(2, initial_state="10")
    assert qs.get_amplitudes()[2] == 1
    assert np.sum(qs.get_amplitudes()) == 1


def test_init_amplitudes():
    qs = QuantumState(2, initial_amplitudes=amplitudes)
    assert np.equal(qs.get_amplitudes(), np.array([0.12, 0, 0, 1])).all()


def test_is_normalized_false():
    qs = QuantumState(2, initial_amplitudes=amplitudes)
    assert not qs.is_normalized()


def test_is_normalized_true():
    qs = QuantumState(2, initial_state="10")
    assert qs.is_normalized()


def test_normalize():
    qs = QuantumState(2, initial_amplitudes=amplitudes)
    assert not qs.is_normalized()
    qs.normalize()
    assert qs.is_normalized()


def test_unique_sat_solver():
    qs = quantum.unique_sat_solver(unique_circuit, 4, 1)
    assert qs.get_amplitudes()[1] == 2.75


def test_unique_sat_solver_k():
    qs = quantum.unique_sat_solver(unique_circuit, 4, 4)
    assert qs.get_amplitudes()[1] == 3.05078125
