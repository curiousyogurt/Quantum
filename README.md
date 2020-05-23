# Quantum Circuit for Grover's Algorithm
Grover.py simulates Grover's Algorithm (a quantum circuit) on a classical computer using Python and the QuTiP library.  Grover's Algorithm is an  unstructured search algorithm.  For this script, we take an <input_string>, which is a string of 0s (the "haystack"), with the exception of a single 1 (the "needle").  The goal of the algorithm is to determine the position of the needle.

Here is an overview of the quantum circuit that makes up Grover's Algorithm for two qubits plus a control qubit.

    |0> H --+----+-- H X . X H ------- M
    |0> H --| Uf |-- H X Z X H ------- M
    |1> H --+----+-------------- H X ---

## Prerequisites

The script runs under Python 3.8.2, and assumes the following libraries are available:

* Qutip : 4.5.1  (http://qutip.org)
* Scipy : 1.4.1  (https://www.scipy.org)
* Numpy : 1.18.4 (https://numpy.org)

## Using Grover.py

From the command line:
`python Grover.py`

1. Without any modifications, the script creates a random search problem with a single target, and uses a simulated circuit to discover the target.
2. The code is heavily commented and intended for educational purposes.  Sometimes several methods will be given for a single objective (these have been flagged in the code).

