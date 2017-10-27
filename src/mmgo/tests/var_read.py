# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import re
import simplexquery as sxq
import myunittest

class VarRead(myunittest.TestCase):
	def test_k(self):
		self.assertEqual(
			sxq.execute("<body>{string(/generatedTop/T/goroutine/k)}</body>",
				self.config),
			"<body> 42 </body>")
		pass

class VarReadSc(VarRead):
		pass

class VarReadDw(VarRead):
	def test_hb(self):
		pass

	def test_shadowed(self):
		pass
