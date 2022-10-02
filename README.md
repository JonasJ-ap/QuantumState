# QuantumState

A package for quantum computation.

## Requirement

 - Numpy 1.21.5
 - Scipy 1.9.1

## Example Usage

```
from quantum import QuantumState

qs = QuantumState(2) # create a quantum state containing 2 qubits

qs.hadamard_all() # perform hadamard operation on all qubits

qs.if_then_minus(lambda x: x == int("0001",2)) # perform if F(A, B) then minus operation.

```
