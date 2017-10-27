# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
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
	def factory(semantics, test, config):
		'''Returns a test object for appropriate test & semantics 
		with the given configuration'''
		assert(semantics[0:5] == 'mmgo-')
		exec('import ' + test)
		cmd = test + '.' + myunittest.get_class_name(semantics, test) \
					+ '(config="' + config + '")'
		return (eval(cmd)) # create an instance an return

	@staticmethod
	def get_class_name(semantics, test):
		assert(semantics[0:5] == 'mmgo-')
		return (test+' '+semantics[5:len(semantics)]).title().replace(' ','').replace('_','')

	@staticmethod
	def get_test_names(semantics, test):
		assert(semantics[0:5] == 'mmgo-')
		exec('import ' + test)
		test_loader = unittest.TestLoader()
		test_names = test_loader.getTestCaseNames(eval(test + '.' 
								+ myunittest.get_class_name(semantics, test)))
		return test_names

	@staticmethod
	def get_test_suite(semantics, test, config, dry_run=False):
		assert(semantics[0:5] == 'mmgo-')
		exec('import ' + test)
		test_names = myunittest.get_test_names(semantics, test)
		suite = unittest.TestSuite()
		for test_name in test_names:
			if dry_run:
				print(test_name)
				continue
			cmd = test + "." + myunittest.get_class_name(semantics, test) + "('"  \
							+ test_name + "', config='" + config.strip() + "')"
			suite.addTest(eval(cmd))
		return suite

	@staticmethod
	def main(semantics, test, config):
		suite = myunittest.get_test_suite(semantics, test, config)
		unittest.TextTestRunner().run(suite)
