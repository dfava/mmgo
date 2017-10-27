import simplexquery as sxq
import myunittest

class SeqComp(myunittest.TestCase):
	def test_k(self):
		self.assertEqual(
			sxq.execute("<body>{string(/generatedTop/T/goroutine/k)}</body>",
				self.config),
			"<body> 3 </body>")
		pass

class SeqCompSc(SeqComp):
		pass

class SeqCompDw(SeqComp):
		pass
