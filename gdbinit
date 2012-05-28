# Instructions:
#   Save as ~/.gdbinit

python
import sys
sys.path.insert(0, '~/src/gdb-codesize/')
from disassemble import function_size
from disassemble import function_until
end

# Disable height-based pagination
set height 0

