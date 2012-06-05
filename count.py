#!/usr/bin/env python

import re
import sys

# How many offset bits are in a page. 12 means 4KiB pages.
PAGE_LOG_SIZE = 12
PAGE_SIZE = 1 << PAGE_LOG_SIZE
PAGE_MASK = 0xffffffffffffffffff & (0xffffffffffffffffff << PAGE_LOG_SIZE)

def count_pages(data):
  pages = {}
  keys = sorted(data.keys(), key=lambda s: data[s][0])
  total_size = 0

  for k in keys:
    start = data[k][0]
    end = data[k][1]
    size = data[k][2]

    s = start & PAGE_MASK
    e = end & PAGE_MASK

    total_size += end - start

    if size <= PAGE_SIZE:
      pages[ s ] = 1
      pages[ e ] = 1
    else:
      r = range(s, end+1, PAGE_SIZE)

      for page in r:
        pages[page] = 1

  return pages,total_size


def parse(text):
  r = re.compile(r"\('0x([0-9a-f]+)', '0x([0-9a-f]+)'\) \('([^']+)', ([0-9]+)\)")

  lines = text.split("\n")
  data = [r.match(l) for l in lines]
  data = [d.groups() for d in data if d is not None]

  results = {}

  for start,end,name,length in data:
    results[name] = (int(start,16),
                     int(end,16),
                     int(length))

  return results

if __name__ == "__main__":
  if len(sys.argv) == 1:
    print """Usage:
  count.py <filename>

  where <filename> is a file produced by disassemble.py in GDB."""
    sys.exit(1)

  text = open(sys.argv[1]).read()
  s = parse(text)
  p,c = count_pages(s)

  print "Pages of code:", len(p)
  print "Size of code:", c/1024.
  print "Functions:", len(s.keys())


