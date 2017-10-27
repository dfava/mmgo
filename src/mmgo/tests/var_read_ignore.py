# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import re
import simplexquery as sxq
import myunittest

class VarReadIgnore(myunittest.TestCase):
	def test_k(self):
		self.assertEqual(
			sxq.execute("<k>{string(/generatedTop/T/goroutine/k)}</k>",
				self.config),
			"<k> 1 </k>")
		pass


class VarReadIgnoreSc(VarReadIgnore):
		pass

class VarReadIgnoreDw(VarReadIgnore):
		pass
