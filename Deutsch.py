#############################################################################
# This script implements Deutsch's Algorithm.  Deutsch's Algorithm is a
# deterministic quantum algorithm devised by David Deutsch in 1985 that
# functions as a proof of concept, in that the quantum circuit runs in fewer
# steps than does the classical algorithm.
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
#     Section 1.4.3, pp. 32–34.
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
# gate.  Uf is the oracle (which encodes function f).  At M, we measure only
# the top qubit.  If we measure the top qubit in state |0>, we know f is
# constant;  if we measure the top qubit in state |1>, we know f is balanced.
##############################################################################

from qutip.qip.operations import *
from qutip.qip.circuit import *
from qutip import basis, tensor, sigmax, qeye, Qobj
from numpy import *

##############################################################################
# Set up and run circuit
##############################################################################

def circuit(input_string='11'):

    ##############################################################################
    # First, set the input string, depending on f.  It must be one of the
    # following options.  input_string is just a fancy way of describing f.
    # '00' means an output of 0 (first digit) for f(0), followed by an output of 0
    # (second digit) for f(1); similarly for the others.
    ##############################################################################
    # input_string = '00' # Constant - f(x) = 0
    # input_string = '11' # Constant - f(x) = 1
    # input_string = '01' # Balanced = f(x) = x
    # input_string = '10' # Balanced = f(x) = not-x
    ##############################################################################

    ##############################################################################
    # Set up all the elements necessary to execute the quantum circuit of
    # Deutsch's Algorithm, and run the algorithm.
    ##############################################################################

    # Top (q0) and bottom (q1) qubits
    q0 = basis(2,0) # top qubit in state |0>
    q1 = basis(2,1) # bottom qubit in state |1>

    # Gates used in the algorithm
    I = qeye(2) # identity gate (quantum wire)
    H = hadamard_transform(1) # Hadamard gate
    NOT = sigmax() # NOT (X) gate
    CNOT = cnot() # CNOT gate

    ##############################################################################
    # Construct Uf gate based on input_string according to the following schema:
    # '00' ==> identity (quantum wire) on top and bottom qubits
    # '11' ==> identity on top qubit, NOT (X) on bottom qubit
    # '01' ==> CNOT (control on top qubit)
    # '10' ==> CNOT (control on top qubit), followed by identity on the top qubit,
    #          and NOT on the bottom qubit
    ##############################################################################

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
    return ({'input_string': input_string,
        'result': result})

##############################################################################
# Interpret and print results.
##############################################################################

def results(input_string, result):

    print('-' * 60)
    print("|00>", result[0][0])
    print("|01>", result[1][0])
    print("|10>", result[2][0])
    print("|11>", result[3][0])
    print('-' * 60)

    probability_00_01 = round(result[0][0][0]**2 + result[1][0][0]**2). real
    probability_10_11 = round(result[2][0][0]**2 + result[3][0][0]**2). real

    # Measuring |00> or |01> means the top qubit is in state |0>
    print('Probability of measuring |00> or |01>: ', probability_00_01)
    # Measuring |10> or |11> means the top qubit is in state |1>
    print('Probability of measuring |10> or |11>: ', probability_10_11)

    if probability_00_01 == 1.0:
        print("Interpretation: Constant (top qubit measured in state |0>)")
        if (input_string == '00' or input_string == '11'):
            print("Function      : Constant (confirmed)")
        else:
            print("Error (interpretation does not match function)")
    elif probability_10_11 == 1.0:
        print("Interpretation: Balanced (top qubit measured in state |1>)")
        if (input_string == '10' or input_string == '01'):
            print("Function      : Balanced (confirmed)")
        else:
            print("Error (interpretation does not match function)")
    else:
        print("Error (unable to interpret)")

    print('-' * 60)

##############################################################################
# Main
##############################################################################

# Get output of the circuit, based on an input string (default is '11');
# valid inputs are '00', '11' (constant) or '01', '10' (balanced).  See
# comments above for more detail.
output = circuit('11')

# Interpret and print results of running the circuit
results(output['input_string'],output['result'])
