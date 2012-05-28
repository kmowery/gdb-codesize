import json
import re
import pprint

def d():
  import gdb
  disassembly = gdb.execute("disassemble $pc", False, True)
  function_size(disassembly)

def do_disassembly(s1, s2):
  filere = re.compile("[0-9]+\s+in\s+(.*)")

  m1 = filere.match(s1)
  m2 = filere.match(s2)

  if m1 is not None and m2 is not None:
    return m1.groups(1) != m2.groups(1)

  return s1 != s2


def function_until(end, filename=None):
  import gdb
  reend = re.compile(end)
  functions = {}

  i = 0

  last_function = None
  s = gdb.execute("step", False, True)

  vfprintf_count = 0

  while(last_function is None or not reend.search(last_function)):
    lines = s.split("\n")
    #print lines

    if last_function is None or do_disassembly(last_function, lines[0]):
      print "the line: \"%s\""%(lines[0])
      #print "last_function: \"%s\""%(last_function)
      #print "lines: ", lines
      #print

      disassembly = gdb.execute("disassemble $pc", False, True)
      loc = function_size(disassembly)
      functions[str( tuple(loc[0:2]) )] = loc[2:]
      print loc[2]

      i = i + 1
      if filename is not None and i % 100 == 0:
        f = open(filename, "w+") if filename is not None else None
        for key,item in functions.iteritems():
          f.write( str(key) + " " + str(item) + "\n" )
        f.close()

        bt = gdb.execute("backtrace", False, True)
        print
        print bt
        print


    last_function = lines[0]

    if "convertUTF8ToUTF16" in last_function or \
       "readUTF8Sequence" in last_function or \
       "__memcpy_ssse3" in last_function or \
       "__memset_sse2" in last_function or \
       "__memcmp_sse4" in last_function or \
       "(anonymous namespace)::ParsePath" in last_function or \
       "DoPartialPath" in last_function or \
       "WTF::StringImpl::create" in last_function or \
       "DoRemoveURLWhitespace" in last_function:
      s = gdb.execute("finish", False, True)

    if "vfprintf.c" in last_function:
      vfprintf_count += 1
      if vfprintf_count > 100:
        s = gdb.execute("finish", False, True)


    s = gdb.execute("step", False, True)

  print functions

  #disassembly = gdb.execute("disassemble $pc", False, True)
  #loc = function_size(disassembly)

def function_size(disassembly):
  newline = re.compile("\n")
  whitespace = re.compile("\s+")
  linesre = re.compile(".*(0x[0-9a-f]+)[\t\s]+<([-+][0-9]+)>:[\t\s]+.*")

  lines = newline.split(disassembly.strip())
  function_name = re.compile("Dump of assembler code for function (.*):").match(lines[0]).group(1)

  lines = lines[1:-1]

  matches = [linesre.match(l.strip()) for l in lines]

  #print [l.strip() for l in lines]
  #print matches

  size = (int(matches[-1].group(2))+1)
  begin = matches[0].group(1)
  end = matches[-1].group(1)

  return (begin,end,function_name,size)

if __name__ == "__main__":
  print function_size(
"""Dump of assembler code for function main:
	0x00000000004004f4 <+0>:		 push	 %rbp
	0x00000000004004f5 <+1>:		 mov		%rsp,%rbp
=> 0x00000000004004f8 <+4>:		 sub		$0x10,%rsp
	0x00000000004004fc <+8>:		 movl	 $0x1,-0x4(%rbp)
	0x0000000000400503 <+15>:		mov		$0x40060c,%edi
	0x0000000000400508 <+20>:		callq	0x4003f0 <puts@plt>
	0x000000000040050d <+25>:		mov		$0x0,%eax
	0x0000000000400512 <+30>:		leaveq
	0x0000000000400513 <+31>:		retq
End of assembler dump.""")

