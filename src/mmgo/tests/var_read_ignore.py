# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import re
import simplexquery as sxq
import myunittest

class Common(myunittest.TestCase):
	def test_k(self):
		self.assertEqual(
			sxq.execute("<k>{string(/generatedTop/T/goroutine/k)}</k>",
				self.config),
			"<k> 1 </k>")
		pass

class Dw(Common):
	def test_hb(self):
		pass
