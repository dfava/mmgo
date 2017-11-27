# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import os
import sys
import imp
import ast 
import inspect
import unittest
import simplexquery as sxq

class TestCase(unittest.TestCase):
	def __init__(self, methodName='runTest', config=None):
		super(TestCase, self).__init__(methodName)
		self.config = config

	def test_hb(self):
		'''A test for happens before assuming an mmgo-sc semantics.
		The subclasses for different semantics are suposed to overide this.'''
		res = sxq.execute_all("/generatedTop/T/goroutine/sigma/HB", self.config)
		for r in res:
			self.assertEqual(r, '<HB> .Map </HB>')
		pass

	def test_shadowed(self):
		'''A test for shadowed assuming an mmgo-sc semantics.
		The subclasses for different semantics are suposed to overide this.'''
		res = sxq.execute_all("/generatedTop/T/goroutine/sigma/S", self.config)
		for r in res:
			self.assertEqual(r, '<S> .Set </S>')
		pass


class myunittest():
	@staticmethod
	def check(semantics, mmgo_program, configuration, dry_run=False, output=None):
		assert(semantics[0:5] == 'mmgo-')
		(mmgo_prog_path,mmgo_prog_name) = os.path.split(mmgo_program)
		mod_name = os.path.splitext(mmgo_prog_name)[0]
		try:
			(fhandle, fname, details) = imp.find_module(mod_name, [mmgo_prog_path])
		except ImportError:
			return # Did not find a corresponding .py file for the mmgo test
		mod = imp.load_module(mod_name, fhandle, fname, details)
		p = ast.parse(inspect.getsource(mod))
		classes = [kls.name for kls in p.body if isinstance(kls, ast.ClassDef)]
		assert("Common" in classes)
		# See if a the test class specific to the semantics exist
		# If it doesn't, use the 'Common' test class
		test_class_name = semantics[5:len(semantics)].title()
		if test_class_name not in classes:
			test_class_name = "Common"
		kls = getattr(mod, test_class_name)
		test_loader = unittest.TestLoader()
		test_names = test_loader.getTestCaseNames(kls)
		suite = unittest.TestSuite()
		for test_name in test_names:
			if dry_run:
				print(test_name)
				continue
			suite.addTest(kls(test_name, config=configuration.strip()))
		res = unittest.TextTestRunner(stream=output).run(suite)
		return res

	@staticmethod
	def main(semantics, test, config):
		myunittest.check(semantics, test, config)
