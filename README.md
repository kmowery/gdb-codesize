# GDB Code Size Analysis

This small script discovers approximately how much code runs to support a
particular function call. Using the GDB Python interface, it disassembles
interesting functions and records their size.

## Getting Started

1. Edit `~/.gdbinit` and insert the code from `/gdbinit`. Change the path on
   line 6 as necessary.

2. Debug your program under GDB and set a breakpoint in the function you're
   instrumenting.

3. In the GDB console, do:

     > python function_until("<fname>", "~/filename")

   where <fname> is the function upon which to stop (I recommend using the
   caller of the function with the breapoint). The second argument is the
   location where the results will be stored for later analysis.

4. Run `count.py` on the file you created in the previous step.

## Why would I use this?

I wrote this script to compute the size of the code loaded by a running process,
in order to compute the approximate cache pressure simply due to executing code.
This number is surprisingly large, especially in well-architected C++ programs
with polymorphism, constructors, and smart pointers.

## Acknowledgements

This entire idea was lifted from disussion with alexras, and his
gdb-thread-names[https://github.com/alexras/gdb-thread-names].

