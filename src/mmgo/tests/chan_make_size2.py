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

	def test_c_type(self):
		self.assertEqual(
			sxq.execute("<type>{string(/generatedTop/C/chan/type)}</type>",
				self.config),
			"<type> bool </type>")
		pass

	def test_c_forwardq(self):
		self.assertEqual(
			sxq.execute("<forward>{string(/generatedTop/C/chan/forward)}</forward>",
				self.config),
			"<forward> .List </forward>")
		pass

	def test_c_backwardq(self):
		# Make sure there are two items on the backward queue
		res = sxq.execute("<backward>{string(/generatedTop/C/chan/backward)}</backward>",
				self.config)
		m = re.search("<backward> ListItem \(.*\) ListItem \(.*\) </backward>", res)
		self.assertIsNotNone(m)
		pass
