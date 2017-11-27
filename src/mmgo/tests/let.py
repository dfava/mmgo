# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import simplexquery as sxq
import myunittest

class Common(myunittest.TestCase):
	def test_k(self):
		self.assertEqual(
			sxq.execute("<body>{string(/generatedTop/T/goroutine/k)}</body>",
				self.config),
			"<body> ( 1 + 2 ) </body>")
		pass
