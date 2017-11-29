# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import myunittest

class Common(myunittest.TestCase):
	def test_k(self):
		self.assertEqual(len(self.config.goroutines), 1)
		self.assertEqual(self.config.goroutines[0].k, "$panic")
		pass

	def test_c_type(self):
		self.assertEqual(len(self.config.channels), 1)
		self.assertEqual(self.config.channels[0].type, int)
		pass

	def test_c_forwardq(self):
		# The item that was sent and the eot are in the foward queue
		self.assertEqual(self.config.channels[0].forward, 
			[['$eot', {}, set()], [10, {}, set()]])
		pass

	def test_c_backwardq(self):
		# One dummy item in the backward queue
		self.assertEqual(self.config.channels[0].backward, [[{}, set()]])
		pass


if __name__ == "__main__":
	config = { "mmgo-sc" : '''
<generatedTop>
	<T>
		<goroutine>
			<k> $panic </k>
			<sigma>
				<HB> .Map </HB>
				<S> .Set </S>
			</sigma>
		</goroutine>
	</T>
	<W> .Map </W>
	<C>
		<chan>
			<ref> 1 </ref>
			<type> int </type>
			<forward> ListItem ( ListItem ( $eot ) ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( 10 ) ListItem ( .Map ) ListItem ( .Set ) ) </forward>
			<backward> ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) </backward>
		</chan>
	</C>
</generatedTop>''',
							"mmgo-dw" : '''
<generatedTop>
	<T>
		<goroutine>
			<k> $panic </k>
			<sigma>
				<HB> .Map </HB>
				<S> .Set </S>
			</sigma>
		</goroutine>
	</T>
	<W> .Map </W>
	<C>
		<chan>
			<ref> 1 </ref>
			<type> int </type>
			<forward> ListItem ( ListItem ( $eot ) ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( 10 ) ListItem ( .Map ) ListItem ( .Set ) ) </forward>
			<backward> ListItem ( ListItem ( .Map ) ListItem ( .Set ) ) </backward>
		</chan>
	</C>
</generatedTop>''' }
	test = __file__[0:-2] + 'mmgo'
	semantics = "mmgo-sc"; myunittest.myunittest.check(semantics, test, config[semantics]) 
	semantics = "mmgo-dw"; myunittest.myunittest.check(semantics, test, config[semantics])
