#! /usr/bin/env python3
# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import io 
import os
import sys
import argparse
import subprocess

import kprint
from myunittest import myunittest

def CompletedProcess_to_str(res):
	if res.returncode == 0:
		if res.stderr == None or len(res.stderr) == 0: 
			return "PASS"
		else:
			return "WARNING"
	else:
		return "FAIL"


def TextTestResult_to_str(res):
	if len(res.errors) != 0 or len(res.failures) != 0:
		return "FAIL"
	else:
		return "PASS"


def build(mmgo_dir, mmgo_bin, dry_run=False, debug=False):
	cmd_lst = ["kompile", mmgo_bin + ".k"]
	if dry_run:
		print("cd " + mmgo_dir)
	if dry_run or debug:
		print(" ".join(cmd_lst))
	if dry_run: # Create a dummy CompletedProcess object
		res = subprocess.CompletedProcess(args="", returncode=0)
	else:
		res = subprocess.run(cmd_lst, cwd=mmgo_dir)
	return res


def run(mmgo_dir, program, dry_run=False, debug=False):
	cmd_lst = ["krun", program]
	if dry_run:
		print("cd " + mmgo_dir)
	if dry_run or debug:
		print(" ".join(cmd_lst))
	if dry_run: # Create a dummy CompletedProcess object
		res = subprocess.CompletedProcess(args="", returncode=0)
	else:
		res = subprocess.run(cmd_lst, cwd=mmgo_dir, stdout=subprocess.PIPE,
													stderr=subprocess.PIPE, encoding="utf-8")
	return res


def check_TODO_remove_OLD(semantics, program, configuration, dry_run=False):
	import unittest
	# Update python path if needed
	mmgo_program_path = os.path.dirname(os.path.abspath(program))
	if mmgo_program_path not in sys.path:
		sys.path.append(mmgo_program_path)
	# Try to import unittest
	module_name = os.path.splitext(program)[0]
	if not os.path.isfile(module_name + ".py"):
		return
	suite = myunittest.get_test_suite(semantics, module_name, configuration,
					dry_run)
	output = io.StringIO()
	res = unittest.TextTestRunner(stream=output).run(suite)
	return res


def main():
	mmgo_bin = "mmgo"
	parser = argparse.ArgumentParser()
	parser.add_argument("semantics", help="which semantics to use")
	parser.add_argument("programs", nargs="+", help="mmgo program(s) to run")
	parser.add_argument("-k", help="kompile before running",
											action="store_true")
	parser.add_argument("-d", help="dry run", action="store_true")
	parser.add_argument("-v", help="set verbose", action="store_true")
	args = parser.parse_args()
	end = "\n" if args.d else ""
	mmgo_dir = os.path.dirname(os.path.realpath(__file__)) \
							+ os.sep + ".." + os.sep + "src" + os.sep + "k" + os.sep
	mmgo_dir += args.semantics
	if args.k: # Build the semantics before running
		print("kompile " + args.semantics + "... ", end=end, flush=True)
		ret = build(mmgo_dir, mmgo_bin, args.d)
		print(CompletedProcess_to_str(ret))
		if ret.returncode != 0:
			return
	statuses = []
	for program in args.programs:
		print("Running " + program + "... ", end=end, flush=True)
		ret = run(mmgo_dir, os.path.abspath(program), args.d)
		res = myunittest.check(args.semantics, program, None if args.d else ret.stdout.replace("<-","&lt;-"), args.d, output = io.StringIO())
		check_failed = res != None and (len(res.errors) != 0 or len(res.failures) != 0)
		if (check_failed and args.v) \
				or (res != None and len(args.programs) == 1):
			print(res.stream.getvalue())
		if len(args.programs) == 1:
			if not args.d:
				print()
				if ret.stdout != '':
					print(kprint.pprint([ret.stdout]))
			if ret.stderr != None and len(ret.stderr) != 0:
				print(ret.stderr.strip())
		if res == None:
			statuses.append(CompletedProcess_to_str(ret))
		else:
			statuses.append(TextTestResult_to_str(res))
		print(statuses[-1])
	if len(statuses) > 1:
		print("Pass: %d" % statuses.count("PASS"))
		print("Warn: %d" % statuses.count("WARNING"))
		print("Fail: %d" % statuses.count("FAIL"))
	return 0


if __name__ == "__main__":
	sys.exit(main())
