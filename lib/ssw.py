#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, re
from optparse import OptionParser

def exec_shell(defines, executes, workdir, is_debug=False):
  source = "cd " + workdir + "\n"  + "".join(map(str, defines)) + "".join(map(str, executes))
  if is_debug:
    print(source)
  os.system(source)

def apply_defines(defines, options, args, mapper):
  return [apply_define(d, options, args, mapper) for d in defines if d.count('=') == 1]

def apply_define(define, options, args, mapper):
  try:
    xs = define.split('=')
    name = xs[0]
    value = re.sub('\$\{(\d+)\}', lambda m:str(args[int(m.group(1)) - 1]),xs[1])
    return name + '=' + value + "\n"
  except IndexError:
    raise ValueError("This line paramater is not found.(" + define.replace("\n", "") + ")")

def parse_defines(defines, optparser):
  options = {}
  for define in defines:
    name = define.split("=")[0]
    if define.count('=') == 1:
      xs = define.split("#@")
      if len(xs) == 2:
        opts = [s.strip() for s in xs[1].split(",")]
        if opts != []:
          optparser.add_option(opts[0], opts[1], help=opts[2])
          options[name] = opts
  return options

def parse_description(descripts):
  usage = ""
  for line in descripts:
    if line.count("@usage:"):
      usage = "usage:" + line.split("@usage:")[1].replace("\n", "")

  return usage

def parse(input):
  descripts = []
  defines = []
  executes = []
  lines = []

  for line in input:
    lines.append(line,)
    target = line.replace(" ", "").replace("\n", "")
    if target == "#@descript:":
      lines = descripts
    elif target == "#@define:":
      lines = defines
    elif target == "#@main:":
      lines = executes

  return descripts, defines, executes

# 
# main
#

# parse
descripts, defines, executes = parse(sys.stdin)
usage = parse_description(descripts)
optparser = OptionParser(usage = usage)
mapper = parse_defines(defines, optparser)

optparser.add_option("--ssw.debug", action="store_true", default=False, help="ssw debug mode.")
optparser.add_option("--ssw.workdir", default=".", help="working directory.")
(options, args) = optparser.parse_args()

is_debug = vars(options)["ssw.debug"]
workdir = str(vars(options)["ssw.workdir"])

(options, args) = optparser.parse_args()
is_debug = vars(options)["ssw.debug"]


try:
  # apply
  applied_defines = apply_defines(defines, vars(options), args, mapper)

  # execute
  exec_shell(applied_defines, executes, workdir, is_debug)
except Exception, e:
  print(e.message)
  print
  optparser.print_help()
  if is_debug:
    raise

