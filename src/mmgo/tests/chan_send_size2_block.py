# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import simplexquery as sxq

import myunittest

class Common(myunittest.TestCase):
	def test_k(self):
		self.assertEqual(
			sxq.execute("<k>{string(/generatedTop/T/goroutine/k)}</k>",
				self.config),
			"<k> channel ( 1 ) &lt;- 6 </k>")
		pass

	def test_c_forwardq(self):
		self.assertEqual(
			sxq.execute("<forward>{string(/generatedTop/C/chan/forward)}</forward>",
				self.config),
			"<forward> ListItem ( ListItem ( 17 ) ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( 42 ) ListItem ( .Map ) ListItem ( .Set ) ) </forward>")

	def test_c_backwardq(self):
		self.assertEqual(
			sxq.execute("<backward>{string(/generatedTop/C/chan/backward)}</backward>",
				self.config),
			"<backward> .List </backward>")
		pass
