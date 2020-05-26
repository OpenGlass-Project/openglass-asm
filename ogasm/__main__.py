#!/usr/bin/env python3
import sys
from textwrap import wrap
from . import full_assemble

with open(sys.argv[1], 'r') as f:
    code = f.read()

with open(sys.argv[2], 'w+') as f:
    f.buffer.write(full_assemble(code))

exit(0)
