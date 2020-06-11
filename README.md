# Quantum Circuits: Deutsch's Algorithm and Grover's Algorithm

Deutsch.py and Grover.py simulate quantum circuits (Deutsch's Algorithm and Grover's Algorithm respectively) on a classical using Python and the QuTiP library.The code is heavily commented and intended for educational purposes.  In the code for Grover's Algorithm, sometimes several methods will be given for a single objective (these have been flagged in the code).

## Requirements

The scripts runs under Python 3.8.2, and assumes the following libraries are available:

* Qutip : 4.5.1  (http://qutip.org)
* Scipy : 1.4.1  (https://www.scipy.org)
* Numpy : 1.18.4 (https://numpy.org)

## Deutsch's Algorithm

Deutsch's Algorithm  is a deterministic qunatum algorithm devised by David Deutsch in 1985 that functions as a proof of concept, in that the quantum circuit runs in fewer steps than does the classical algorithm.  Given a function f with inputs and outputs 0 and 1 only, the problem is to determine whether f is constant, that is f(0)=0, f(1)=0, or f(0)=1, f(1)=1; or whether f is balanced, that is f(0)=0, f(1)=1, or f(0)=1, f(1)=0.  A classical computer solves this problem by querying f twice (once with 0 as input; once with 1 as input).  Deutsch's Algorithm demonstrates that a quantum computer only needs one query.

Here is an overview of the quantum circuit that implements Deutsch's Algorithm:

            +----+
    |0> H --| Uf |-- H ------- M
    |1> H --|    |------------
            +----+
### Using Deutsch.py

From the command line:
`python Deutsch.py`

Without any modifications, the script runs for a constant f: f(0)=1, f(1)=1.

## Grover's Algorithm

Grover's Algorithm is an unstructured search algorithm.  For this script, we take an <input_string>, which is a string of 0s (the "haystack"), with the exception of a single 1 (the "needle").  The goal of the algorithm is to determine the position of the needle.

Here is an overview of the quantum circuit that makes up Grover's Algorithm for two qubits plus a control qubit.

    |0> H --+----+-- H X . X H ------- M
    |0> H --| Uf |-- H X Z X H ------- M
    |1> H --+----+-------------- H X ---

### Using Grover.py

From the command line:
`python Grover.py`

Without any modifications, the script creates a random search problem with a single target, and uses a simulated circuit to discover the target.
