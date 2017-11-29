# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import myunittest

class Common(myunittest.TestCase):
	pass

class Sc(Common):
	def test_w(self):
		self.assertEqual(self.config.w['x'], 17)
		self.assertEqual(self.config.w['y'], 24)
		pass

class Dw(Common):
	def test_hb(self):
		w = self.config.w
		hb = self.config.goroutines[0].sigma['hb']
		for var in w.keys():
			self.assertEqual(set(w[var].keys()), hb[var])
		pass

	def test_shadowed(self):
		w = self.config.w
		shadowed = self.config.goroutines[0].sigma['s']
		for s in shadowed:
			if s in w['x'].keys():
				self.assertIn(w['x'][s], [0, 42])
			elif s in w['y'].keys():
				self.assertIn(w['y'][s], [0, 42])
			else:
				self.assertFalse(True, "Must never get here")
		pass

	def test_w(self):
		ordered_events = sorted(self.config.w['x'].items())
		self.assertEqual(ordered_events[0][1], 0)  # initial value of 0
		self.assertEqual(ordered_events[1][1], 42) # write of 42
		self.assertEqual(ordered_events[2][1], 17) # write of 17

		ordered_events = sorted(self.config.w['y'].items())
		self.assertEqual(ordered_events[0][1], 0)  # initial value of 0
		self.assertEqual(ordered_events[1][1], 24)  # initial value of 24
		pass


if __name__ == "__main__":
	config = { "mmgo-sc" : '''
<generatedTop>
	<T>
		<goroutine>
			<k> $unit </k>
			<sigma>
				<HB> .Map </HB>
				<S> .Set </S>
			</sigma>
		</goroutine>
	</T>
	<W> x |-> 17 y |-> 24 </W>
	<C> .ChanCellBag </C>
</generatedTop>''',
							"mmgo-dw" : '''
<generatedTop>
	<T>
		<goroutine>
			<k> $unit </k>
			<sigma>
				<HB> x |-> ( SetItem ( 2 ) SetItem ( 6 ) SetItem ( 10 ) ) y |-> ( SetItem ( 3 ) SetItem ( 9 ) ) </HB>
				<S> SetItem ( 2 ) SetItem ( 3 ) SetItem ( 6 ) </S>
			</sigma>
		</goroutine>
	</T>
	<W> x |-> ( 2 |-> 0 6 |-> 42 10 |-> 17 ) y |-> ( 9 |-> 24 3 |-> 0 ) </W>
	<C> .ChanCellBag </C>
</generatedTop>''' }
	test = __file__[0:-2] + 'mmgo'
	semantics = "mmgo-sc"; myunittest.myunittest.check(semantics, test, config[semantics]) 
	semantics = "mmgo-dw"; myunittest.myunittest.check(semantics, test, config[semantics])
