# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import simplexquery as sxq

import k2py
import myunittest

class Common(myunittest.TestCase):
	pass

class Sc(Common):
	def test_write_events(self):
		res = sxq.execute("<W>{string(/generatedTop/W)}</W>", self.config)
		res = res.replace('&gt;', '>')[3:-4]
		w = k2py.translate(res)
		self.assertEqual(w, {'x' : 17, 'y' : 24})
		pass

class Dw(Common):
	def test_hb(self):
		res = sxq.execute("<W>{string(/generatedTop/W)}</W>", self.config)
		res = res.replace('&gt;', '>')[3:-4]
		w = k2py.translate(res)
		res = sxq.execute("<W>{string(/generatedTop/T/goroutine/sigma/HB)}</W>", self.config)
		res = res.replace('&gt;', '>')[3:-4]
		hb = k2py.translate(res)	
		for var in ['x', 'y']:
			self.assertEqual(set(w[var].keys()), hb[var])
		pass

	def test_shadowed(self):
		res = sxq.execute("<W>{string(/generatedTop/W)}</W>", self.config)
		res = res.replace('&gt;', '>')[3:-4]
		w = k2py.translate(res)
		res = sxq.execute("<W>{string(/generatedTop/T/goroutine/sigma/S)}</W>", self.config)
		res = res.replace('&gt;', '>')[3:-4]
		shadowed = k2py.translate(res)	
		for s in shadowed:
			if s in w['x'].keys():
				self.assertIn(w['x'][s], [0, 42])
			elif s in w['y'].keys():
				self.assertIn(w['y'][s], [0, 42])
			else:
				self.assertFalse(True, "Must never get here")
		pass

	def test_write_events(self):
		res = sxq.execute("<W>{string(/generatedTop/W)}</W>", self.config)
		res = res.replace('&gt;', '>')[3:-4]
		d = k2py.translate(res)
		ordered_events = sorted(d['x'].items())
		self.assertEqual(ordered_events[0][1], 0)  # initial value of 0
		self.assertEqual(ordered_events[1][1], 42) # write of 42
		self.assertEqual(ordered_events[2][1], 17) # write of 17

		ordered_events = sorted(d['y'].items())
		self.assertEqual(ordered_events[0][1], 0)  # initial value of 0
		self.assertEqual(ordered_events[1][1], 24)  # initial value of 24
		pass
