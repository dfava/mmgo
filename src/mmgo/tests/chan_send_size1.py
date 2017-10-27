import simplexquery as sxq

import myunittest

class ChanSendSize1(myunittest.TestCase):
	def test_k(self):
		self.assertEqual(
			sxq.execute("<k>{string(/generatedTop/T/goroutine/k)}</k>",
				self.config),
			"<k> $unit </k>")
		pass

class ChanSendSize1Sc(ChanSendSize1):
	pass

class ChanSendSize1Dw(ChanSendSize1):
	pass
