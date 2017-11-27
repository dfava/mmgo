# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import re
import simplexquery as sxq
import myunittest

class Common(myunittest.TestCase):
	def test_k(self):
		self.assertEqual(
			sxq.execute("<body>{string(/generatedTop/T/goroutine/k)}</body>",
				self.config),
			"<body> 42 </body>")
		pass

class Dw(Common):
	def test_hb(self):
		pass

	def test_shadowed(self):
		pass
