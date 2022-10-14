'''
A cocotb-pytest test (this file) has two parts:

1. Testbench 
    - Any python function decorated with @cocotb.test()
    - Drives signals into pins of the design, reads the output/intermediate pins and compares with expected results
    - Uses async-await: 
        - Declared as def async
        - when "await Event()", simulator advances in simulation time until the Event() happens
    - You can have multiple such testbenches too. Pytest would find and run them all
2. PyTest 
    - The setup that connects the simulator of your choice, 
    - Feeds the design files, 
    - Finds your testbenches (1), 
    - Parametrizes them to generate multiple versions of the designs & tests
    - Runs all such tests and prints a report of pass & fails
'''


import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ClockCycles

import random
# import numpy as np

'''
1. Testbench
'''
@cocotb.test()
# async def register_tb(dut):
async def alu_4_bit_tb(dut):

    ''' Clock Generation '''
#     clock = Clock(dut.clk, 10, units="ns") # create a clock for dut.clk pin with 10 ns period
#     cocotb.start_soon(clock.start()) # start clock in a seperate thread

    ''' Assign random values to input, wait for a clock and verify output '''
#     for i in range(100): # 100 experiments
#     for i in range(1): # 100 experiments
        
#         exact = random.randint(0, 255) # generate randomized input
#         dut.d.value = exact # drive pins
    i = 0
    # Addition test
    A_i = 3
    B_i = 4
    S_i = 1 # Addition
    exact = A_i + B_i

    dut.A_i.value = A_i # drive pins
    dut.B_i.value = B_i # drive pins
    dut.S_i.value = S_i # drive pins

#         await FallingEdge(dut.clk) # wait for falling edge
    await Timer(10, units="ns")
#         computed = dut.q.value.integer # Read pins as unsigned integer.
    # computed = dut.q.value.signed_integer # Read pins as signed integer.
    computed = dut.Y_o.value # Read pins as unsigned integer
    
    assert exact == computed, f"Failed on the {i}th cycle. Got {computed}, expected {exact}" # If any assertion fails, the test fails, and the string would be printed in console
#         assert x == computed, f"Random injected asserrtion fail, Failed on the {i}th cycle. Got {computed}, expected {x}" # If any assertion fails, the test fails, and the string would be printed in console
    print(f"Driven value: {exact} \t received value: {computed}") 
    
    # Multiplication test
    A_i = 3
    B_i = 4
    S_i = 0b11 # Multiplication
    exact = A_i * B_i

    dut.A_i.value = A_i # drive pins
    dut.B_i.value = B_i # drive pins
    dut.S_i.value = S_i # drive pins

#         await FallingEdge(dut.clk) # wait for falling edge
    await Timer(10, units="ns")
#         computed = dut.q.value.integer # Read pins as unsigned integer.
    # computed = dut.q.value.signed_integer # Read pins as signed integer.
    computed = dut.Y_o.value # Read pins as unsigned integer
    
    assert exact == computed, f"Failed on the {i}th cycle. Got {computed}, expected {exact}" # If any assertion fails, the test fails, and the string would be printed in console
#         assert x == computed, f"Random injected asserrtion fail, Failed on the {i}th cycle. Got {computed}, expected {x}" # If any assertion fails, the test fails, and the string would be printed in console
    print(f"Driven value: {exact} \t received value: {computed}") 
    
    # Left Shift test
    A_i = 3
    B_i = 4
    S_i = 0b10 # Left Shift
    exact = A_i << B_i  # 3 << 4 = 48 

    dut.A_i.value = A_i # drive pins
    dut.B_i.value = B_i # drive pins
    dut.S_i.value = S_i # drive pins

#         await FallingEdge(dut.clk) # wait for falling edge
    await Timer(10, units="ns")
#         computed = dut.q.value.integer # Read pins as unsigned integer.
    # computed = dut.q.value.signed_integer # Read pins as signed integer.
    computed = dut.Y_o.value # Read pins as unsigned integer
    
    assert exact == computed, f"Failed on the {i}th cycle. Got {computed}, expected {exact}" # If any assertion fails, the test fails, and the string would be printed in console
#         assert x == computed, f"Random injected asserrtion fail, Failed on the {i}th cycle. Got {computed}, expected {x}" # If any assertion fails, the test fails, and the string would be printed in console
    print(f"Driven value: {exact} \t received value: {computed}") 
    
    # Concatenation test
    A_i = 1
    B_i = 1
    S_i = 0b00 # Left Shift
    exact = 0b0001_0001  # {A,B} 

    dut.A_i.value = A_i # drive pins
    dut.B_i.value = B_i # drive pins
    dut.S_i.value = S_i # drive pins

#         await FallingEdge(dut.clk) # wait for falling edge
    await Timer(10, units="ns")
#         computed = dut.q.value.integer # Read pins as unsigned integer.
    # computed = dut.q.value.signed_integer # Read pins as signed integer.
    computed = dut.Y_o.value # Read pins as unsigned integer
    
    assert exact == computed, f"Failed on the {i}th cycle. Got {computed}, expected {exact}" # If any assertion fails, the test fails, and the string would be printed in console
#         assert x == computed, f"Random injected asserrtion fail, Failed on the {i}th cycle. Got {computed}, expected {x}" # If any assertion fails, the test fails, and the string would be printed in console
    print(f"Driven value: {exact} \t received value: {computed}") 



'''
2. Pytest Setup
'''

from cocotb_test.simulator import run
import pytest
import glob

@pytest.mark.parametrize(
    # Two sets of parameters to test across
    "parameters", [
        {"WIDTH_IN": "8", "WIDTH_OUT": "16"},
        {"WIDTH_IN": "16"}
        ])
# def test_register(parameters):
def test_alu_4_bit(parameters):

    run(
#         verilog_sources=glob.glob('register/hdl/*'),
        verilog_sources=glob.glob('alu_4_bit/hdl/*'),
#         toplevel="register",    # top level HDL
        toplevel="alu_4_bit",    # top level HDL
        
#         module="test_register", # name of the file that contains @cocotb.test() -- this file
        module="test_alu_4_bit", # name of the file that contains @cocotb.test() -- this file
        simulator="icarus",

        parameters=parameters,
        extra_env=parameters,
#         sim_build="register/sim_build/" + ",".join((f"{key}={value}" for key, value in parameters.items())),
        sim_build="alu_4_bit/sim_build/" + ",".join((f"{key}={value}" for key, value in parameters.items())),
    )
