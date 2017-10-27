import simplexquery as sxq
import myunittest

class Let(myunittest.TestCase):
	def test_k(self):
		self.assertEqual(
			sxq.execute("<body>{string(/generatedTop/T/goroutine/k)}</body>",
				self.config),
			"<body> ( 1 + 2 ) </body>")
		pass

class LetSc(Let):
	pass

class LetDw(Let):
	pass
