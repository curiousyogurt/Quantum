# Quantum Circuits

Deutsch.py, Deutsch-Jozsa.py, and Grover.py simulate quantum circuits (Deutsch's Algorithm, the Deutsch-Jozsa Algorithm, and Grover's Algorithm respectively) on a classical using Python and the QuTiP library.  The code is heavily commented and intended for educational purposes.  For Grover's Algorithm, sometimes several methods will be given for a single objective (these have been flagged in the code).

For more information on the Deutsch-Jozsa Algorithm, consider: Nielsen, Michael A. and Isaac L. Chung. _Quantum Computation and Quantum Information_.  10th Anniversary Edition.  Cambridge: Cambridge University Press.  See section 1.4.3 for Deutsch, 1.4.4 for Deutsch-Jozsa, and 6.2 Grover.

## Requirements

The scripts runs under Python 3.8.2, and assumes the following libraries are available:

* Qutip : 4.5.1  (http://qutip.org)
* Scipy : 1.4.1  (https://www.scipy.org)
* Numpy : 1.18.4 (https://numpy.org)

## Deutsch's Algorithm

Deutsch's Algorithm  is a deterministic quantum algorithm devised by David Deutsch in 1985 that functions as a proof of concept, in that the quantum circuit runs in fewer steps than does the classical algorithm.  Given a function f with inputs and outputs 0 and 1 only, the problem is to determine whether f is constant, that is f(0)=0, f(1)=0, or f(0)=1, f(1)=1; or whether f is balanced, that is f(0)=0, f(1)=1, or f(0)=1, f(1)=0.  A classical computer solves this problem by querying f twice (once with 0 as input; once with 1 as input).  Deutsch's Algorithm demonstrates that a quantum computer only needs one query.

Here is an overview of the quantum circuit that implements Deutsch's Algorithm:

            +----+
    |0> H --| Uf |-- H ------- M
    |1> H --|    |--------------
            +----+
### Using Deutsch.py

From the command line:
`python Deutsch.py`

Without any modifications, the script runs for a constant f: f(0)=1, f(1)=1, and uses the simulated circuit to determine f is constant.

## The Deutsch-Jozsa Algorithm

The Deutsch-Jozsa Algorithm is a general version of Deutsch's Algorithm.  Deutsch-Jozsa is a deterministic quantum algorithm devised by David Deutsch and Richard Jozsa in 1992.  Supposing we have a string adhering to one of the following patterns: all 0s or all 1s (called "constant") or an equal number of 0s and 1s (called "balanced").

Here is an overview of the quantum circuit that makes up the Deutsch-Jozsa Algorithm for two qubits plus a control qubit.

    |0> H --+----+-- H ------- M
    |0> H --| Uf |-- H ------- M
    |1> H --+----+--------------

### Using Deutsch-Jozsa.py

From the command line:
`python Deutsch-Jozsa.py`

Without any modifications, the script runs for a string of '01010101' (balanced).

## Grover's Algorithm

Grover's Algorithm is an unstructured search algorithm.  For this script, we take an <input_string>, which is a string of 0s (the "haystack"), with the exception of a single 1 (the "needle").  The goal of the algorithm is to determine the position of the needle.

Here is an overview of the quantum circuit that makes up Grover's Algorithm for two qubits plus a control qubit.

    |0> H --+----+-- H X . X H ------- M
    |0> H --| Uf |-- H X Z X H ------- M
    |1> H --+----+-------------- H X ---

### Using Grover.py

From the command line:
`python Grover.py`

Without any modifications, the script creates a random search problem with a single target, and uses the simulated circuit to discover the target.
