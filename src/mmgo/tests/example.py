# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import simplexquery as sxq

import myunittest
import k2py

class Example(myunittest.TestCase):
	def test_k(self):
		res = sxq.execute_all("/generatedTop/T/goroutine/k", self.config)
		expected = ["<k> 1 </k>", "<k> $unit </k>"]
		for r in res:
			self.assertIn(r, expected)
			expected.remove(r)
		pass

class ExampleSc(Example):	
	pass

class ExampleDw(Example):	
	def test_hb(self):
		res = sxq.execute_all("/generatedTop/T/goroutine/sigma/HB", self.config)
		expected = {'x' : set([2, 4])}
		for r in res:
			r = r[4:-5].replace('&gt;', '>')
			hb = k2py.translate(r)
			self.assertEqual(hb, expected)
		pass

	def test_hb(self):
		pass

	def test_shadowed(self):
		pass
