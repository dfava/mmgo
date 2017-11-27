# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import simplexquery as sxq

import myunittest

class Common(myunittest.TestCase):
	def test_k(self):
		self.assertEqual(
			sxq.execute("<k>{string(/generatedTop/T/goroutine/k)}</k>",
				self.config),
			"<k> pend ( 1 ) </k>")
		pass
