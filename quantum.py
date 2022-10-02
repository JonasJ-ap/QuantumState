import numpy as np
import scipy as sp

BINARY = 2
PROP_INITIAL_STATE = "initial_state"
PROP_INITIAL_AMPLITUDE = "initial_amplitude"

AVG_DIV_RATIO = 0.5
HADAMARD_RATIO = np.sqrt(0.5)


def string_to_amplitudes(s: str) -> np.ndarray:
    str_inner = s[1:-1]
    str_seq = str_inner.split(',')
    result_state = np.zeros(len(str_seq))
    for i in range(len(str_seq)):
        result_state[i] = int(str_seq[i])
    return result_state


class QuantumState:

    def __init__(self, bit_num, **properties):
        self.bitNum = bit_num
        self.dim = 2 ** bit_num
        self.state = np.zeros(self.dim)
        if PROP_INITIAL_STATE in properties and PROP_INITIAL_AMPLITUDE in properties:
            raise ValueError(f"Cannot set both initial state and amplitude")
        if PROP_INITIAL_STATE in properties:
            if len(properties[PROP_INITIAL_STATE]) != bit_num:
                raise ValueError(f"Initial state must have {bit_num} bits")
            self.state[int(properties[PROP_INITIAL_STATE], BINARY)] = 1
        else:
            self.state[0] = 1

        if PROP_INITIAL_AMPLITUDE in properties:
            self.state = string_to_amplitudes(properties[PROP_INITIAL_AMPLITUDE])

    def get_amplitudes(self):
        return self.state

    def get_bit_num(self):
        return self.bitNum

    def add_diff_all(self):
        self.state = np.matmul(sp.linalg.hadamard(self.dim), self.state.T)
        return self

    def avg_div_all(self):
        self.state = np.matmul((AVG_DIV_RATIO ** self.bitNum) * sp.linalg.hadamard(self.dim), self.state.T)
        return self

    def hadamard_all(self):
        self.state = np.matmul((HADAMARD_RATIO ** self.bitNum) * sp.linalg.hadamard(self.dim), self.state.T)
        return self

    def if_then_minus(self, f):
        def function_wrapper(f1, index, amplitude):
            bool_result = f1(index)
            if bool_result:
                return -amplitude
            else:
                return amplitude

        self.state = np.array(list(map(lambda x, y: function_wrapper(f, x, y), range(self.dim), self.state)))
        return self

    def if_xor_then_minus(self, b):
        def xor_quantum(index, amplitude):
            if sum([int(digit) for digit in bin((index & b))[2:]]) % 2 == 0:
                return -amplitude
            else:
                return amplitude

        self.state = np.array(list(map(lambda x, y: xor_quantum(x, y), range(self.dim), self.state)))
        return self

    def reflection_across_the_mean(self):
        self.avg_div_all()
        self.state[1:] = -self.state[1:]
        self.add_diff_all()
        return self


def analyze_function(f, argc):
    qs = QuantumState(argc)
    qs.add_diff_all().if_then_minus(f).avg_div_all()
    return qs


def ifBias(f, argc):
    qs = analyze_function(f, argc)
    return qs[0] == 0


def unique_sat_solver(f, argc, k):
    qs = QuantumState(argc)
    qs.add_diff_all()
    for _ in range(k):
        qs = qs.if_then_minus(f)
        qs = qs.reflection_across_the_mean()
    return qs
