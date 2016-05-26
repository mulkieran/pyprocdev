pyprocdev
=========

This package supplies a Python interface to the /proc/devices file.

To use, instantiate the ProcDev class and invoke its methods. ::

    >>> from pyprocdev import *
    >>> procdev = ProcDev()
    >>> procdev.majors(DeviceTypes.BLOCK)
    [8, 9, 11, 65, 66, 67, 68, 69, 70, 71, 128, 129, 130, 131, 132, 133, 134, 135, 253, 254, 259]
    >>> procdev.majors(DeviceTypes.CHARACTER)
    [1, 4, 5, 7, 10, 13, 14, 21, 29, 99, 116, 128, 136, 162, 166, 180, 188, 189, 202, 203, 226, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254]
    >>> procdev.drivers(DeviceTypes.BLOCK)
    frozenset(['md', 'sr', 'device-mapper', 'blkext', 'mdp', 'sd'])
    >>> procdev.get_driver(DeviceTypes.BLOCK, 8)
    'sd'
    >>> procdev.get_majors(DeviceTypes.BLOCK, 'sd')
    [8, 65, 66, 67, 68, 69, 70, 71, 128, 129, 130, 131, 132, 133, 134, 135]
