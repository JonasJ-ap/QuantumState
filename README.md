# QuantumState

A package for quantum computation.


## Example Usage

```
import quantum

qs = QuantumState(2) # create a quantum state containing 2 bits

qs.hadamard_all() # perform hadamard operation on all bits

qs.if_then_minus(lambda x: x == int("0001",2)) # perform if F(A, B) then minus operation.

```