# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import simplexquery as sxq

import myunittest

class Common(myunittest.TestCase):
	def test_k(self):
		res = sxq.execute_all("/generatedTop/T/goroutine/k", self.config)
		self.assertEqual(res[0], "<k> 42 </k>")
		self.assertEqual(res[1], "<k> $unit </k>")
		pass

	def test_c_forwardq(self):
		self.assertEqual(
			sxq.execute("<forward>{string(/generatedTop/C/chan/forward)}</forward>",
				self.config),
			"<forward> .List </forward>")

	def test_c_backwardq(self):
		self.assertEqual(
			sxq.execute("<backward>{string(/generatedTop/C/chan/backward)}</backward>",
				self.config),
			"<backward> .List </backward>")
		pass
