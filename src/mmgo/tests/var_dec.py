# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import simplexquery as sxq
import myunittest

class Common(myunittest.TestCase):
	def test_shadowed_init(self):
		# Make sure shadowed set is empty
		self.assertEqual(
				sxq.execute("<S>{string(/generatedTop/T/goroutine/sigma/S)}</S>",
					self.config),
				"<S> .Set </S>")
		pass

class Dw(Common):
	def test_hb_init(self):
		# Make sure declared variables are in the happened before set
		res = sxq.execute("<HB>{string(/generatedTop/T/goroutine/sigma/HB)}</HB>", self.config)
		self.assertIn('x |-&gt;', res)
		self.assertIn('y |-&gt;', res)
		self.assertIn('z |-&gt;', res)
		pass

	def test_write_events_init(self):
		# Make sure there exist write events for the declared variables
		res = sxq.execute("<W>{string(/generatedTop/W)}</W>", self.config)
		self.assertIn('x |-&gt;', res)
		self.assertIn('y |-&gt;', res)
		self.assertIn('z |-&gt;', res)
		pass

	def test_hb(self):
		pass
