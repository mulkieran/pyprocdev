# Copyright (C) 2016 Anne Mulhern
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Anne Mulhern <amulhern@redhat.com>

"""
Pyprocdev main class.
"""
import itertools

from ._errors import ProcDevParsingError
from ._errors import ProcDevValueError

from ._constants import DeviceTypes


class _TablePairs(object):
    """
    Tables that are inverses of each other.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, left, right):
        """
        Initializer.

        :param left: table mapping x to y
        :param rigth: table mapping y to xs
        """
        self.left = left
        self.right = right


class ProcDev(object):
    """
    Main class for /proc/devices data.
    """

    def _parse_file(self, filepath='/proc/devices'):
        """
        Parse the file, initializing data structures.

        :param str filepath: the filepath to parse

        :raises ProcDevParsingError:
        """
        parsing = DeviceTypes.NOTYPE
        with open(filepath) as istream:
            for line in istream:
                line = line.rstrip()

                if line == "":
                    parsing = DeviceTypes.NOTYPE
                    continue

                if line == "Character devices:":
                    parsing = DeviceTypes.CHARACTER
                    continue

                if line == "Block devices:":
                    parsing = DeviceTypes.BLOCK
                    continue

                try:
                    (major, device) = line.split()
                except ValueError:
                    raise ProcDevParsingError(
                       "Unexpected format for line %s" % line
                    )

                try:
                    table = self._tables[parsing].left
                except KeyError:
                    raise ProcDevParsingError(
                       "Parsing data for unknown device type %s." % parsing
                    )

                table[int(major)] = device

    def __init__(self, filepath='/proc/devices'):
        """
        Initializer.

        :param str filespath: the filepath from which to read the data

        :raises: ProcDevError on failure
        """
        self._tables = {
           DeviceTypes.CHARACTER : _TablePairs(dict(), None),
           DeviceTypes.BLOCK : _TablePairs(dict(), None)
        }

        self._parse_file(filepath)

    def get_driver(device_type, major_number):
        """
        Get the driver name for ``major_number``.

        :param DeviceType device_type: the device type
        :param int major_number: the major number

        :returns: the drive name for this major number or None if none
        :rtype: str or NoneType

        :raises ProcDevValueError: for bad device type
        """
        try:
            table = self._tables[device_type]
        except KeyError:
            raise ProcDevValueError(device_type, "device_type")

        try:
            return table.left[major_number]
        except KeyError:
            return None

    def _build_reverse_table(self, table):
        """
        Build a table that reverses ``table``.

        :param table: a mapping from x to y

        :returns: a table that reverses the mapping
        :rtype: dict of y * (set of x)
        """
        items = sorted(table.items(), lambda x: x[1])
        groups = itertools.groupby(items, lambda x: x[1])

        return dict(
           (key, frozenset(x[0] for x in pairs)) for key, pairs in groups
        )

    def get_majors(device_type, driver):
        """
        Get the major numbers for ``driver``.

        :param DeviceType device_type: the device type
        :param str driver: the name of the driver

        :returns: the set of major numbers corresponding to this driver
        :rtype: set of int or NoneType

        :raises ProcDevValueError: for a bad device type
        """
        try:
            table_pair = self._tables[device_type]
        except KeyError:
            raise ProcDevValueError(device_type, "device_type")

        table_pair.right = \
           table_pair.right or self._build_reverse_table(table_pair.left)

        return table_pair.right.get(driver)
