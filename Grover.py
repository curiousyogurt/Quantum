#############################################################################
# This script implements Grover's Algorithm.  Grover's Algorithm is an
# unstructured search algorithm.  For this script, we take an <input_string>,
# which is a string of 0s (the "haystack"), with the exception of a single
# 1 (the "needle").  The goal of the algorithm is to determine the position
# of the needle.
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
# This script is intended for learning purposes, and is heavily commented.
# At times, there are multiple methods to accomplish a single goal.  These
# have been flagged, and you may swap out one method for another.
#
# Here is an overview of the quantum circuit that makes up Grover's Algorithm
# for two qubits plus a control qubit.
#
# |0> H --+----+-- H X . X H ------- M
# |0> H --| Uf |-- H X Z X H ------- M
# |1> H --+----+-------------- H X ---
#
# The qubits all begin in state |0>, except for the control qubit that begins
# in state |1>.  H is the Hadamard gate.  Uf is a phase inversion that flips
# the sign of the element represented by the needle.  The sequence of gates
# in the middle, H/X/Controlled-Z/X/H is an inversion about the mean.  Then
# we apply H and X to the control qubit.  At M, we measure all the qubits
# except for the control qubit.
#
# The structure of this script is:
#
# Part One:   Generate the <input_string> and call needle_init()
# Part Two:   Set up Qubits and Gates
# Part Three: Execute the circuit
# Part Four:  Results and Interpretation
##############################################################################

from qutip.qip.operations import *
from qutip.qip.circuit import *
from qutip import basis, tensor, sigmax, qeye, Qobj
from numpy import *

#############################################################################
# Part One: Generate input_string and call needle_init()
#############################################################################

# In Part One, we generate <input_string>, which is composed entirely of 0s,
# except for a single 1 that represents the item we are searching for in the
# string.  The length of <input_string> should be a power-of-2, which is
# important to note for needle_explicit(); the string can always be padded
# with additional 0s if necessary.

# Method 1.  Randomly generated.    Call needle_random()
# Method 2.  Explicitl assignment.  Call needle_explicit()
# Method 3.  Position in binary.    Call needle_binary()
# Method 4.  Position in decimal.   Call needle-decimal()

#-----------------------------------------------------------------------------
# Function: needle_random(max)
#-----------------------------------------------------------------------------
# Generate input_string randomly, on the basis of a random integer.
#-----------------------------------------------------------------------------
# max: the upper limit for the random integer, as a power of 2.
#-----------------------------------------------------------------------------
def needle_random(max=5):
    random_length       = 2 ** random.randint(1,max)
    random_input_string = '0' * random_length
    random_needle       = random.randint(0,random_length-1)
    random_input_string = (random_input_string[:random_needle] + '1' +
                          random_input_string[random_needle + 1:])
    input_string        = random_input_string
    return input_string

#-----------------------------------------------------------------------------
# Function: needle_explicit(input_string)
#-----------------------------------------------------------------------------
# Generate input_string randomly, on the basis of an explicit string.
# Remember that the string length must be a power-of-2.
#-----------------------------------------------------------------------------
# input_string: the string to return
#-----------------------------------------------------------------------------
def needle_explicit(input_string = '0010' + ('0' * 60)):
    # Suggestions:
    # 128: input_string = '0010' + ('0' * 124)
    # 256: input_string = '0010' + ('0' * 252)
    # 512: input_string = '0010' + ('0' * 508)
    return input_string

#-----------------------------------------------------------------------------
# Function: needle_binary(binary_needle_position)
#-----------------------------------------------------------------------------
# Generate input_string randomly, on the basis of binary position.
#-----------------------------------------------------------------------------
# binary_needle_position: the position in binary
#-----------------------------------------------------------------------------
def needle_binary(binary_needle_position = '0100'):
    decimal_needle_position = int(binary_needle_position, 2)
    input_string_length     = 2**math.ceil(math.log(decimal_needle_position+1,2))
    input_string            = '0' * decimal_needle_position
    input_string            = input_string + '1'
    input_string            = input_string + '0' * (input_string_length -
                                                    decimal_needle_position - 1)
    return input_string

#-----------------------------------------------------------------------------
# Function: needle_decimal()
#-----------------------------------------------------------------------------
# Generate input_string randomly, on the basis of decimal position.
#-----------------------------------------------------------------------------
# decimal_needle_position: the position in decimal
#-----------------------------------------------------------------------------
def needle_decimal(decimal_needle_position = 5):
    input_string_length     = 2**math.ceil(math.log(decimal_needle_position+1,2))
    input_string            = '0' * decimal_needle_position
    input_string            = input_string + '1'
    input_string            = input_string + '0' * (input_string_length -
                                                   decimal_needle_position - 1)
    return input_string

#-----------------------------------------------------------------------------
# Function: needle_init()
#-----------------------------------------------------------------------------
# Initialise the needle position based on input_string
#-----------------------------------------------------------------------------
def needle_init(input_string):

    # Given <input_string>, get the length and calculate the required number
    # of qubits to process string.
    input_string_length = input_string.__len__()
    required_qubits     = int(math.log(input_string_length,2))

    # Get the needle position.  We will use this to generate gates and state
    # various results.
    needle_position      = input_string.find('1')
    needle_binary        = binary_repr(needle_position, required_qubits)
    needle_binary_length = needle_binary.__len__()

    return ({'string': input_string,
            'string_length': input_string_length,
            'required_qubits': required_qubits},
            {'position': needle_position,
            'binary': needle_binary,
            'binary_length': needle_binary_length})

##############################################################################
# Part Two: Set up Qubits and Gates
##############################################################################

# In Part Two, we set up all the elements necessary to execute the quantum
# circuit of Grover's Algorithm.  Call circut() to set up the following:
#
# qubits - Array of all qubits (including control)
# Q      - Qubits in combined state
# H      - Hadamard gates for all qubits
# UfXI   - Phase inversion using with I on control
# CxNOT  - Controlled NOT on all gates
# HxI    - Hadamard gates for all except I on control
# XxI    - X gates for all except I on control
# CxZI   - Controlled Z on all gates with I on control
# IxH    - H on control
# IxX    - X on control
#
# Uf     - Created using UfXI and CxNOT
# Dif    - Created using HxI, Xx, and CxZI

# As a final step in Part Two, we calculate a value for repeat, which
# determines how many times the circuit loops in order to maxmise the
# chance of identifying the position of the needle.

#-----------------------------------------------------------------------------
# Function: circuit()
#-----------------------------------------------------------------------------
# Initialise the elements of the circuit (qubits and gates)
#
# A note on variable naming conventions for matrices: a capital letter is a
# collection of the same sort of thing.  So 'Q' means qubits all the way down,
# and 'H' means Hadamards all the way down.  A small 'x' is a greedy wildcard,
# so 'HxI' means Hadamards all the way down except Identity at the bottom.
# 'CxNOT' means controls (C) all the way down except NOT at the bottom.
#-----------------------------------------------------------------------------
def circuit(input,needle):
    # ------
    # qubits
    # ------
    #
    # Create an array of qubits.  An input string of length n requires n^2 qubits
    # beginning in state |0>, plus a control qubit that begins in state |1>.
    qubits=[]
    for i in range(input['required_qubits']):
        qubits.append(basis(2,0)) # 0 qubit
    qubits.append(basis(2,1))     # 1 qubit (control)

    # ------
    # Q
    # ------
    #
    # All qubits put into a combined state with tensor multiplication
    Q = None
    for qubit in qubits:
        if Q:
            Q = tensor(Q,qubit)
        else:
            Q = tensor(qubit)

    # ------
    # H
    # ------
    #
    # Hadamards as a combined operation for all qubits
    H = None
    for qubit in qubits:
        if H:
            H = tensor(H,hadamard_transform(1))
        else:
            H = hadamard_transform(1)

    # ------
    # Uf
    # ------
    # There are two different methods we have for generating Uf:
    #
    # Method 1: Buliding Uf from more primitive qunatum gates.  Call uf1().
    # Method 2: Directly descirbing the matrix for Uf.  Call uf2().
    #
    # We include both methods, because each provides some insight.

    #-----------------------------------------------------------------------------
    # Function: uf1()
    #-----------------------------------------------------------------------------
    # Method 1 for Generating the Uf (= phase inversion) Gate
    #-----------------------------------------------------------------------------
    def uf1():

        # Uf may be done in a number of ways.  The first is to break down Uf a
        # follows: (i) a combined state representing the item we are looking for in
        # binary, (ii) a controlled not where all qubits are control except for the
        # last qubit which is the not; (iii) the same combined state as (i).
        #
        # |> -----.-----
        # |> -- X . X --
        # |> ---- + ----
        #
        # We do this by creating UfXI which correpsonds to (i) and (iii), and CxNOT
        # which corresponds to (ii).  We can then combine (UfXI * CxNOT * UfXI) to get
        # Uf.

        # Calculate the binary value that corresponds to the position of the item to
        # be found (which we call the needle).  Then, go through that binary number:
        # each 0 will correspond to an X gate; each 1 will correspond to an I gate.
        # So if the third (of four items) is the needle, this gives us 010, which
        # corresponds to [X I X].  Finish off UfXI by including an identity gate for
        # the control qubit.
        #
        # Gates required: UfXI, CxNOT

        UfXI = None
        for i in range(needle['binary_length']):
            if needle['binary'][i] == '0':
                if UfXI:
                    UfXI = tensor(UfXI,sigmax())
                else:
                    UfXI = sigmax()
            else:
                if UfXI:
                    UfXI = tensor(UfXI,qeye(2))
                else:
                    UfXI = qeye(2)
        UfXI = tensor(UfXI,qeye(2))

        # CxNOT as a combined operation.  this is caluclated by a series of identity
        # gates, with a NOT gate in the lower right corner.
        CxNOT = zeros([input['string_length']*2,input['string_length']*2])
        for i in range(input['string_length']-1):
            CxNOT[i*2,i*2] = '1'
            CxNOT[i*2+1,i*2+1] = '1'
        CxNOT[input['string_length']*2-1,input['string_length']*2-2] = '1'
        CxNOT[input['string_length']*2-2,input['string_length']*2-1] = '1'

        # Calculate Uf
        Uf = UfXI * CxNOT * UfXI
        return Uf

    #-----------------------------------------------------------------------------
    # Function: uf2()
    #-----------------------------------------------------------------------------
    # Method 2 for Generating the Uf (= phase inversion) Gate
    #-----------------------------------------------------------------------------
    def uf2():

        # Another way to create Uf is to do so directly, by generating a zero matrix
        # of size n by n and plotting 1s as necessary, according to the following
        # algorithm: 
        Uf = zeros([input['string_length']*2,input['string_length']*2])
        for i in range(input['string_length']):
            if input['string'][i] == '0':
                Uf[i*2,i*2] = '1'
                Uf[i*2+1,i*2+1] = '1'
            else:
                Uf[i*2+1,i*2] = '1'
                Uf[i*2,i*2+1] = '1'
        return Uf

    # Set Uf using uf1() or uf2() (both are equivalent)
    Uf = uf1()

    # ------
    # Dif
    # ------
    # There are two different methods we have for generating Dif; these methods
    # are parallel to how we generated Uf.
    #
    # Method 1: Buliding Dif from more primitive qunatum gates.  Call dif1().
    # Method 2: Directly descirbing the matrix for Uf.  Call dif2().
    #
    # Again, we include both methods, because each provides some insight.

    #-----------------------------------------------------------------------------
    # Function: dif1()
    #-----------------------------------------------------------------------------
    # Method 1 for the Dif (= inversion about the mean) Gate
    #-----------------------------------------------------------------------------
    def dif1():

        # Generate the diffusion operator Dif.  This operator leaves the control qubit
        # untouched, but follows the following pattern for the others:
        #
        # |> -- H X . X H --
        # |> -- H X Z X H --
        #
        # In order to generate this operator, we need to combine Hadamards for each
        # non-control and Identity for control; and Xs for each non-control and
        # Identity for control.  Finally, we have to have a controlled-Z for non-
        # control and Identity for control.  (This operator does not act directly on
        # the control qubit.)
        #
        # Gates required: HxI, XxI, CxZI

        # Hadamards + Identity (for control qubit) as a combined operation
        HxI = None
        for qubit in qubits[:-1]:
            if HxI:
                HxI = tensor(HxI,hadamard_transform(1))
            else:
                HxI = hadamard_transform(1)
        HxI = tensor(HxI,qeye(2))

        # Xs + Identity (for control qubit) as a combined operation
        XxI = None
        for qubit in qubits[:-1]:
            if XxI:
                XxI = tensor(XxI,sigmax())
            else:
                XxI = sigmax()
        XxI = tensor(XxI,qeye(2))

        # CxZ + Identity (for control qubit) as a combined operation
        CxZI = zeros([input['string_length'],input['string_length']])
        for i in range(int(input['string_length']-1)):
            CxZI[i,i] = '1'
        CxZI[input['string_length']-1,input['string_length']-1] = '-1'
        CxZI = tensor(Qobj(CxZI), qeye(2))
        CxZI.dims = HxI.dims

        # Diffusion operator
        Dif = HxI * XxI * CxZI * XxI * HxI
        return Dif

    #-----------------------------------------------------------------------------
    # Function: dif2()
    #-----------------------------------------------------------------------------
    # Method 2 for the Dif (= inversion about the mean) Gate
    #-----------------------------------------------------------------------------
    def dif2():

        # The other way to generate Dif is to calculate -I+2A, where A is the matrix
        # that finds the average sequence (1/2n, where n is the number of qubits * 2)
        # and I is the identity matrix.  The resulting matrix is combined with
        # identity (since it does not act directly on the control qubit).

        A = (1 / (2 ** input['required_qubits'])) * ones([2 ** input['required_qubits'], 2 ** input['required_qubits']])
        Two_A = 2 * A
        Minus_I = -1 * identity(2 ** input['required_qubits'])
        Dif = tensor(Qobj(Minus_I + Two_A), qeye(2))
        return Dif

    # Set Dif using df1() or df2() (both are equivalent)
    Dif = dif1();

    # The final pair of operations are on the control qubit, and this acts on
    # the results to make them more dramatic.  Create two combined operations
    # that act only on control (so the rest will be I): IxH and IxX.
    #
    # Gates required: IxH, IxX

    # ------
    # IxH
    # ------
    # Ix + Hadamard (for control qubit) as a combined operation
    IxH = None
    for qubit in qubits[:-1]:
        if IxH:
            IxH = tensor(IxH,qeye(2))
        else:
            IxH = qeye(2)
    IxH = tensor(IxH,hadamard_transform(1))

    # ------
    # IxX
    # ------
    # Ix + X (for control qubit) as a combined operation
    IxX = None
    for qubit in qubits[:-1]:
        if IxX:
            IxX = tensor(IxX,qeye(2))
        else:
            IxX = qeye(2)
    IxX = tensor(IxX,sigmax())

    # Return a dictonary of qubits and gates
    return {'Q': Q,
            'H': H,
            'Uf': Uf,
            'Dif': Dif,
            'IxH': IxH,
            'IxX': IxX}

#-----------------------------------------------------------------------------
# Function: repeat(required_qubits)
#-----------------------------------------------------------------------------
# Phase inversion (Uf) + the Diffusion operator (Dif) are repeated pi/4 *
# sqrt(2^n) times, where n is the number of qubits (not including control).
# This picks out and then amplifies the result so that the answer is easy to
# see.  Repeat it more times than this, and the numbers will become
# "overcooked" (meaning we move away from the ideal solution).
#-----------------------------------------------------------------------------
# required_qubits: number of loops depend on number of qubits in the circuit
#-----------------------------------------------------------------------------
def repeat(required_qubits):
    # We might think that int(around((pi/4) * sqrt(2**input['required_qubits'])))
    # would be preferable.  But this leads to 2-qubit (+1 control) circuits being
    # run twice instead of once, which overcooks the results.
    return int((pi/4) * sqrt(2**(required_qubits)))

##############################################################################
# Part Three: Execute the circuit
##############################################################################

# In order to run the circuit, we apply the gates to the qubits in their
# combined states.  This is simply matrix multiplication.  Begin by applying
# H to every qubit; then Uf (phase inversion); then Dif (inversion about the
# mean); then finish off by applying H and X to the control.

#-----------------------------------------------------------------------------
# Function: run_circuit(circuit, repeat)
#-----------------------------------------------------------------------------
# Execute the circuit calculations.  Repeat Uf/Dif the appropriate numebr of
# times.
#-----------------------------------------------------------------------------
# circuit: dictionary for the circuit (expected: Q, H, Uf, Dif, IxH, IxX)
# repeat: integer representing the number of times to run Uf/Dif
#-----------------------------------------------------------------------------
def run_circuit(circuit,repeat):
    # Begin with applying H to Q
    current_state = circuit['H'] * circuit['Q']

    # Now repeat Uf and Dif <repeat> times.  This is the Grover Iteration.
    for i in range(repeat):
        current_state = circuit['Uf'] * current_state
        current_state = circuit['Dif'] * current_state
        current_state = Qobj(current_state)
        # Uncomment the following if you want to see the state at each step
        # print("Uf/Dif [", i, "]", current_state)

    # Now apply IxH and IxX.  This is not really requried in order to make
    # Grover's Algorithm work, but it amplifies the results to make them
    # extremely obvious.  If you want to remove this line, replace it with
    # current_state = current_state.full().
    current_state = circuit['IxX'] * circuit['IxH'] * current_state.full()
    return current_state

##############################################################################
# Part Four: Results and Interpretation
##############################################################################

#-----------------------------------------------------------------------------
# Function: results(input, needle, repeat, current_state)
#-----------------------------------------------------------------------------
# Print results to the console.
#-----------------------------------------------------------------------------
# input: dictionary containing string, string_length, required_qubits
# needle: dictionary containing position, binary, binary length
# repeat: integer representing the number of times to run Uf/Dif
# current_state: results after running the circuit
#-----------------------------------------------------------------------------
def results(input,needle,repeat,current_state):
    # Get the indices of the standout values in the matrix.
    max_state = argmax(current_state)
    max_state_value = abs(current_state[max_state,0])
    min_state = argmin(current_state)
    min_state_value = abs(current_state[min_state,0])

    # Setting <result> to half the standout value will give us the position
    # of the 1 <input['string']>.
    if max_state_value > min_state_value:
        result = max_state
        result_value = max_state_value
    else:
        result = min_state
        result_value = min_state_value
    result = int(result/2)

    # Print the combined state, and flag the result
    print('-' * 60)
    print('Combined state:')
    for i in range(current_state.size):
        if i == result*2:
            flag = '*****'
        else:
            flag = ''
        print(binary_repr(i,input['required_qubits']+1), ':', current_state.item(i),flag)

    # Output all results
    print('-' * 60)
    print('Input string             :', input['string'])
    print('Actual Position (decimal):', needle['position'])
    print('Actual Postiion (binary) :', needle['binary'])
    print('Iterations required      :', repeat)
    print('Qubits required          :', input['required_qubits'], '(+1 control)')

    print('State of winning qubit   :', current_state[max_state,0])

    # Double-check by comparing <result> with the index of the 1 in the string.
    # Flag the confirmation or the error.
    check = input['string'].find('1')
    if result == check:
        confirmed = '(confirmed)'
    else:
        confirmed = '(error)'

    # Print results
    print('Calculated position      : {} {}'.format(result,confirmed))
    print('-' * 60)

##############################################################################
# Main
##############################################################################

# Part One: Generate the <input_string> and call needle_init()
input_string = needle_random()
input,needle = needle_init(input_string)

# Part Two: Set up Qubits and Gates
circuit = circuit(input,needle)
repeat = repeat(input['required_qubits'])

# Part Three: Execute the circuit
current_state = run_circuit(circuit,repeat)

# Part Four: Results and Interpretation
results(input,needle,repeat,current_state)
