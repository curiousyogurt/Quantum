#############################################################################
# This script implements Deutsch's Algorithm.  Deutsch's Algorithm is a
# deterministic qunatum algorithm devised by David Deutsch in 1985 that
# functions as a proof of concept, in that the quantum circut runs in fewer
# steps than does the classical algorihm.
#
# The problem is as follows: given function f, with possible inputs 0 and 1,
# and possible outputs 0 and 1, determine whether f is constant or balanced,
# as follows:
#
# f(0)=0, f(1)=0 ==> f is constant
# f(0)=1, f(1)=1 ==> f is constant
# f(0)=0, f(1)=0 ==> f is balanced
# f(0)=1, f(1)=1 ==> f is balanced
#
# A classical computer needs to query f twice (once with input 0, once with
# input 1) to determine whether f is constant or balanced.  A quantum
# computer need query f only once. 
#
# Version information:
#
# Python: 3.8.2
# Qutip : 4.5.1  (http://qutip.org)
# Scipy : 1.4.1  (https://www.scipy.org)
# Numpy : 1.18.4 (https://numpy.org)
#
# For more information on Grover's Algorithm, I suggest:
#   Nielsen, Michael A. and Isaac L. Chung.  2010.
#     _Quantum Computation and Quantum Information_.
#     10th Anniversary Edition.
#     Cambridge: Cambridge University Press.
#     Section 6.2, pp. 255-261.
#
# Here is an overview of the quantum circuit that makes up Deutsch's Algorithm
# for a top and bottom qubit.
#
#         +----+
# |0> H --| Uf |-- H ------- M
# |1> H --|    |------------
#         +----+
#
# The qubits start in state |0> and |1> respectively.  H is the Hadamard
# gate.  Uf is the oracle (which encodes function f).  At M, we meeasure only
# the top qubit.
##############################################################################

from qutip.qip.operations import *
from qutip.qip.circuit import *
from qutip import basis, tensor, sigmax, qeye, Qobj
from numpy import *

##############################################################################
# First, set the input string, depending on f.  It must be one of the
# following options.  input_string is just a fancy way of describing f.
# '00' means an output of 0 (first digit) for f(0), followed by an output of 0
# (second digit) for f(1); similarly for the others.
##############################################################################
# input_string = '00' # Constant - f(x) = 0
# input_string = '11' # Constant - f(x) = 1
# input_string = '01' # Balanced = f(x) = x
input_string = '10' # Balanced = f(x) = not-x

##############################################################################
# Now set up all the elements necessary to execute the quantum circuit of
# Deutsch's Algorithm, and run the algorithm.
##############################################################################

# Top (q0) and bottom (q1) qubits
q0 = basis(2,0) # 0 qubit
q1 = basis(2,1) # 1 qubit

# Gates used in the algorithm
I = qeye(2)
H = hadamard_transform(1)
NOT = sigmax()
CNOT = cnot()

# Determine Uf gate based on input_string according to the following schema:
# '00' identity (quantum wire) on top and bottom qubits
# '11' identity on top qubit, NOT (X) on bottom qubit
# '01' CNOT (control on top qubit)
# '10' CNOT (control on top qubit), followed by identity on the top qubit,
#      and NOT on the bottom qubit
if input_string == '00':
    Uf = tensor(I,I)
elif input_string == '11':
    Uf = tensor(I,NOT)
elif input_string == '01':
    Uf = CNOT
elif input_string == '10':
    Uf = CNOT * tensor(I, NOT)
else:
    print("Input string error")
    raise SystemExit(0)

# Tensors for combined states
Q = tensor(q0,q1)
HH = tensor(H,H)
HI = tensor(H,I)

# Run the quantum circuit
result = HI * Uf * HH * Q

##############################################################################
# Print and interpret results.
##############################################################################

print('-' * 60)
print("|00>", result[0][0])
print("|01>", result[1][0])
print("|10>", result[2][0])
print("|11>", result[3][0])
print('-' * 60)

probability_00_01 = round(result[0][0][0]**2 + result[1][0][0]**2). real
probability_10_11 = round(result[2][0][0]**2 + result[3][0][0]**2). real

print('Probability of measuring |00> or |01>: ', probability_00_01)
print('Probability of measuring |10> or |11>: ', probability_10_11)

if (input_string == '00' or input_string == '11'):
    if probability_00_01 == 1.0:
        print("Interpretation: Constant (top qubit measured in state |0>)")
        print("Function      : Constant (confirmed)")
elif (input_string == '10' or input_string == '01'):
    if probability_10_11 == 1.0:
        print("Interpretation: Balanced (top qubit measured in state |1>)")
        print("Function      : Balanced (confirmed)")
else:
    print("Error")

print('-' * 60)
