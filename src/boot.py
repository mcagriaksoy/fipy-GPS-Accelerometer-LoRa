"""
Mehmet Cagri Aksoy - 2018-2023
This script is executed on boot-up. It imports necessary modules and runs the main.py script.
"""

# boot.py -- run on boot-up
import os

import machine
import pycom

machine.main('main.py')
