# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import myunittest

class Common(myunittest.TestCase):
	def test_k(self):
		self.assertEqual(len(self.config.goroutines), 1)
		self.assertEqual(self.config.goroutines[0].k, "3")
		pass


if __name__ == "__main__":
	config = { "mmgo-sc" : '''
<generatedTop>
	<T>
		<goroutine>
			<k> 3 </k>
			<sigma>
				<HB> .Map </HB>
				<S> .Set </S>
			</sigma>
		</goroutine>
	</T>
	<W> .Map </W>
	<C> .ChanCellBag </C>
</generatedTop>''',
							"mmgo-dw" : '''
<generatedTop>
	<T>
		<goroutine>
			<k> 3 </k>
			<sigma>
				<HB> .Map </HB>
				<S> .Set </S>
			</sigma>
		</goroutine>
	</T>
	<W> .Map </W>
	<C> .ChanCellBag </C>
</generatedTop>''' }
	test = __file__[0:-2] + 'mmgo'
	semantics = "mmgo-sc"; myunittest.myunittest.check(semantics, test, config[semantics]) 
	semantics = "mmgo-dw"; myunittest.myunittest.check(semantics, test, config[semantics])
