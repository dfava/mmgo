# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import re
import simplexquery as sxq
import myunittest

class VarReadUninit(myunittest.TestCase):
	def test_k(self):
		self.assertEqual(
			sxq.execute("<k>{string(/generatedTop/T/goroutine/k)}</k>",
				self.config),
			"<k> 0 </k>")
		pass

class VarReadUninitSc(VarReadUninit):
		pass

class VarReadUninitDw(VarReadUninit):
		pass
