# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import simplexquery as sxq
import myunittest

class GoSimple(myunittest.TestCase):
	def test_multiple_ks(self):
		res = sxq.execute_all("/generatedTop/T/goroutine/k", self.config)#,
		self.assertEqual(res[0], "<k> 6 </k>")
		self.assertEqual(res[1], "<k> 5 </k>")
		pass

class GoSimpleSc(GoSimple):
	pass

class GoSimpleDw(GoSimple):
	def test_hb(self):
		pass

	def test_shadowed(self):
		pass
