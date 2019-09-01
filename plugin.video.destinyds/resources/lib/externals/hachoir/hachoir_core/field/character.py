"""
Character field class: a 8-bit character
"""

from resources.lib.externals.hachoir.hachoir_core.field import Bits
from resources.lib.externals.hachoir.hachoir_core.endian import BIG_ENDIAN
from resources.lib.externals.hachoir.hachoir_core.tools import makePrintable

class Character(Bits):
    """
    A 8-bit character using ASCII charset for display attribute.
    """
    static_size = 8

    def __init__(self, parent, name, description=None):
        Bits.__init__(self, parent, name, 8, description=description)

    def createValue(self):
        return chr(self._parent.stream.readBits(
            self.absolute_address, 8, BIG_ENDIAN))

    def createRawDisplay(self):
        return unicode(Bits.createValue(self))

    def createDisplay(self):
        return makePrintable(self.value, "ASCII", quote="'", to_unicode=True)

