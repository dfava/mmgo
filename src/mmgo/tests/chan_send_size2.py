# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import simplexquery as sxq

import myunittest

class ChanSendSize2(myunittest.TestCase):
	def test_k(self):
		self.assertEqual(
			sxq.execute("<k>{string(/generatedTop/T/goroutine/k)}</k>",
				self.config),
			"<k> $unit </k>")
		pass

class ChanSendSize2Sc(ChanSendSize2):
	pass

class ChanSendSize2Dw(ChanSendSize2):
	pass
