#############################################################################
# Thi script implements the Deutsch-Jozsa Algorithm, which is a general
# version of Deutsch's Algorithm.  The Deutsch-Jozsa Algorithm is a
# deterministic quatum algorithm devised by David Deutsch and Richard Jozsa
# in 1992.
#
# The problem is as follows: given a string, each of whose digits is either
# 0 or 1, with the following pattern: either all 0s, all 1s (constant), or
# an equal number of 0s and 1s (balanced).
#
# Version information:
#
# Python: 3.8.2
# Qutip : 4.5.1  (http://qutip.org)
# Scipy : 1.4.1  (https://www.scipy.org)
# Numpy : 1.18.4 (https://numpy.org)
#
# For more information on the Deutsch-Jozsa Algorithm, I suggest:
#   Nielsen, Michael A. and Isaac L. Chung.  2010.
#     _Quantum Computation and Quantum Information_.
#     10th Anniversary Edition.
#     Cambridge: Cambridge University Press.
#     Section 1.4.4, pp. 34–38.
#
# Here is an overview of the quantum circuit that makes up the Deutsch-Jozsa
# Algorithm for two qubits plus a control qubit.
#
# |0> H --+----+-- H ------- M
# |0> H --| Uf |-- H ------- M
# |1> H --+----+--------------
#
##############################################################################

from qutip.qip.operations import *
from qutip.qip.circuit import *
from qutip import basis, tensor, sigmax, qeye, Qobj
from numpy import *

##############################################################################
# Set up and run circuit
##############################################################################

# Set input_string to be the function input.  The number of characters in the
# string must be a power of 2.  The Deutsch-Jozsa Algorithm requires that this
# string either be all 0s, all 1s (both constant) or an equal number of 0s and
# 1s (balanced, but order does not matter).

def circuit(input_string='01010101'):

    input_string_length = input_string.__len__()
    required_qubits = int(math.log(input_string_length,2))

    # Create an array of qubits.  An input string of length n requires n^2 qubits
    # beginning in state |0>, plus a control qubit that begins in state |1>.
    qubits=[]
    for i in range(required_qubits):
        qubits.append(basis(2,0)) # Qubits in state |0>
    qubits.append(basis(2,1))     # Control qubit in state |1>

    # Qubits put into a combined state with tensor multiplication
    Q = None
    for qubit in qubits:
        if Q:
            Q = tensor(Q,qubit)
        else:
            Q = tensor(qubit)

    # Hadamards as a combined operation
    H = None
    for qubit in qubits:
        if H:
            H = tensor(H,hadamard_transform(1))
        else:
            H = hadamard_transform(1)

    # Hadamards + Identity (for control qubit) as a combined operation
    HI = None
    for qubit in qubits[:-1]:
        if HI:
            HI = tensor(HI,hadamard_transform(1))
        else:
            HI = hadamard_transform(1)
    HI = tensor(HI,qeye(2))

    # Uf is generated by creating a zero matrix of suitable size, then plotting
    # 1s as necessary
    Uf = zeros([input_string_length*2,input_string_length*2])
    for i in range(input_string_length):
        if input_string[i] == '0':
            Uf[i*2,i*2] = '1'
            Uf[i*2+1,i*2+1] = '1'
        else:
            Uf[i*2+1,i*2] = '1'
            Uf[i*2,i*2+1] = '1'

    # Run the quantum circuit
    result = HI*Uf*H*Q
    return ({'input_string': input_string,
        'result': result})

##############################################################################
# Interpret and print results.
##############################################################################

def results(input_string, result):

    print('-' * 60)
    array_length = len(result)
    elements = int(math.log(array_length,2))
    for i in range(array_length):
        print("|" +  "{0:b}".format(i).zfill(elements) + ">" +
                " " + str(result[i][0]. real))
    print('-' * 60)

    winning_elements = "0" * (elements-1)
    probability_winning_elements = result[0] ** 2 + result[1] ** 2

    print("Probability of |" + winning_elements + "0> or |" +
            winning_elements + "1>: " +
            str(round(probability_winning_elements[0]. real)))

    print("Input         :", input_string)

    # Interpret the results: if the first or second qubit is > 0.5 (it will be
    # the inverse of root-2, or 0.70710678), then the function is constant.
    # Otherwise, the function is balanced.
    if (result[0] > 0.5 or result[1] > 0.5):
        print('Interpretation: constant', end='')
        if ((input_string == '1' * len(input_string)) or 
                (input_string == '0' * len(input_string))):
            print(" (confirmed)")
        else:
            print(" (error)")
    else:
        print('Interpretation: balanced', end='')
        if ((input_string != '1' * len(input_string)) or 
                (input_string != '0' * len(input_string))):
            print(" (confirmed)")
        else:
            print(" (error)")
    print('-' * 60)

##############################################################################
# Main
##############################################################################

# Get output of the circuit, based on an input string (default is '01010101');
# valid inputs are, for example, '00000000' or '11111111' (constant) or
# '01010101' (balanced).  See comments above for details.
#
# output = circuit('00000000') # (constant)
# output = circuit('11111111') # (constant)
output = circuit('01010101')

# Interpret and print results of running the circuit
results(output['input_string'],output['result'])
