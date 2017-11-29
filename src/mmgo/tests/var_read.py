# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import myunittest

class Common(myunittest.TestCase):
	def test_k(self):
		self.assertEqual(len(self.config.goroutines), 1)
		self.assertEqual(self.config.goroutines[0].k, "42")
		pass

class Dw(Common):
	def test_hb(self):
		pass

	def test_shadowed(self):
		pass


if __name__ == "__main__":
	config = { "mmgo-sc" : '''
<generatedTop>
	<T>
		<goroutine>
			<k> 42 </k>
			<sigma>
				<HB> .Map </HB>
				<S> .Set </S>
			</sigma>
		</goroutine>
	</T>
	<W> x |-> 42 y |-> 24 </W>
	<C> .ChanCellBag </C>
</generatedTop>''',
							"mmgo-dw" : '''
<generatedTop>
	<T>
		<goroutine>
			<k> 42 </k>
			<sigma>
				<HB> x |-> ( SetItem ( 2 ) SetItem ( 6 ) ) y |-> ( SetItem ( 3 ) SetItem ( 8 ) ) </HB>
				<S> SetItem ( 2 ) SetItem ( 3 ) </S>
			</sigma>
		</goroutine>
	</T>
	<W> x |-> ( 2 |-> 0 6 |-> 42 ) y |-> ( 8 |-> 24 3 |-> 0 ) </W>
	<C> .ChanCellBag </C>
</generatedTop>''' }
	test = __file__[0:-2] + 'mmgo'
	semantics = "mmgo-sc"; myunittest.myunittest.check(semantics, test, config[semantics]) 
	semantics = "mmgo-dw"; myunittest.myunittest.check(semantics, test, config[semantics])

