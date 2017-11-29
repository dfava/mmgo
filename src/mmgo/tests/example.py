# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import myunittest

class Common(myunittest.TestCase):
	def test_k(self):
		self.assertEqual(len(self.config.goroutines), 2)
		self.assertEqual(self.config.goroutines[0].k, "1")
		self.assertEqual(self.config.goroutines[1].k, "$unit")
		pass

class Sc(Common):	
	def test_w(self):
		self.assertEqual(self.config.w, {'x' : 1})
		pass

class Dw(Common):	
	def test_w(self):
		ordered_events = sorted(self.config.w['x'].items())
		self.assertEqual(ordered_events[0][1], 0) # initial value of x
		self.assertEqual(ordered_events[1][-1], 1) # final value of x
		pass

	def test_hb(self):
		ordered_events = sorted(self.config.w['x'].items())
		hb = set([ordered_events[0][0]] + [ordered_events[1][0]]) # expected HB for x
		self.assertEqual(self.config.goroutines[0].sigma['hb']['x'], hb)
		self.assertEqual(self.config.goroutines[1].sigma['hb']['x'], hb)
		pass

	def test_shadowed(self):
		ordered_events = sorted(self.config.w['x'].items())
		s = set([ordered_events[0][0]]) # expected shadowed set
		self.assertEqual(self.config.goroutines[0].sigma['s'], s)
		self.assertEqual(self.config.goroutines[1].sigma['s'], s)
		pass

if __name__ == "__main__":
	config = { "mmgo-sc" : '''
<generatedTop>
	<T>
		<goroutine>
			<k> 1 </k>
			<sigma>
				<HB> .Map </HB>
				<S> .Set </S>
			</sigma>
		</goroutine>
		<goroutine>
			<k> $unit </k>
			<sigma>
				<HB> .Map </HB>
				<S> .Set </S>
			</sigma>
		</goroutine>
	</T>
	<W> x |-> 1 </W>
	<C>
		<chan>
			<ref> 1 </ref>
			<type> int </type>
			<forward> .List </forward>
			<backward> ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) </backward>
		</chan>
	</C>
</generatedTop>''',
							"mmgo-dw" : '''
<generatedTop>
	<T>
		<goroutine>
			<k> 1 </k>
			<sigma>
				<HB> x |-> ( SetItem ( 1 ) SetItem ( 5 ) ) </HB>
				<S> SetItem ( 1 ) </S>
			</sigma>
		</goroutine>
		<goroutine>
			<k> $unit </k>
			<sigma>
				<HB> x |-> ( SetItem ( 1 ) SetItem ( 5 ) ) </HB>
				<S> SetItem ( 1 ) </S>
			</sigma>
		</goroutine>
	</T>
	<W> x |-> ( 1 |-> 0 5 |-> 1 ) </W>
	<C>
		<chan>
			<ref> 3 </ref>
			<type> int </type>
			<forward> .List </forward>
			<backward> ListItem ( ListItem ( x |-> SetItem ( 1 ) ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) </backward>
		</chan>
	</C>
</generatedTop>'''}
	test = __file__[0:-2] + 'mmgo'
	semantics = "mmgo-sc"; myunittest.myunittest.check(semantics, test, config[semantics]) 
	semantics = "mmgo-dw"; myunittest.myunittest.check(semantics, test, config[semantics])
