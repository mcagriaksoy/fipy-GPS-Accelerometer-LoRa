"""
Mehmet Cagri Aksoy - 2018-2023
"""

from pycoproc import Pycoproc

__version__ = '1.4.0'

class Pytrack(Pycoproc):
    """
    Pytrack class for controlling the Pytrack board.

    Args:
        i2c: Optional. The I2C bus object to use for communication.
        sda: Optional. The pin number for the SDA line of the I2C bus.
        scl: Optional. The pin number for the SCL line of the I2C bus.
    """

    def __init__(self, i2c=None, sda='P22', scl='P21'):
        Pycoproc.__init__(self, i2c, sda, scl)
