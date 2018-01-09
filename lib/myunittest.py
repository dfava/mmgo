# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import os
import sys
import imp
import ast 
import inspect
import unittest

import xml2py
import xml.etree.ElementTree as et

class TestCase(unittest.TestCase):
	def __init__(self, methodName='runTest', config=None):
		super(TestCase, self).__init__(methodName)
		self.config = config

	def test_hb(self):
		'''A test for happens before assuming an mmgo-sc semantics.
		The subclasses for different semantics are suposed to overide this.'''
		self.assertGreater(len(self.config.goroutines), 0)
		for gr in self.config.goroutines:
			self.assertEqual(gr.sigma['hb'], {})
		pass

	def best_shadowed(self):
		'''A test for shadowed assuming an mmgo-sc semantics.
		The subclasses for different semantics are suposed to overide this.'''
		self.assertGreater(len(self.config.goroutines), 0)
		for gr in self.config.goroutines:
			self.assertEqual(gr.sigma['s'], {})
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
			try:
				suite.addTest(kls(test_name, config=xml2py.xml2py(configuration)))
			except et.ParseError as e:
				sys.stderr.write("Error parsing the following configuration='%s'\n" % configuration)
				raise e
		res = unittest.TextTestRunner(stream=output).run(suite)
		return res

	@staticmethod
	def main(semantics, test, config):
		myunittest.check(semantics, test, config)
