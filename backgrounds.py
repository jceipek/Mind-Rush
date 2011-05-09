#
# backgrounds.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

from engine.background import Background

class ScrollingCodeBackground(Background):
    def __init__(self):
        Background.__init__(self, (0,0,0))