# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import myunittest
from mmgo import mmgo

class Common(myunittest.TestCase):
  def test_k(self):
    self.assertEqual(len(self.config.goroutines), 2)
    self.assertEqual(self.config.goroutines[1].k, "42")
    self.assertEqual(self.config.goroutines[0].k, "$unit")
    pass

  def test_chans(self):
    # One channels will have backward==forward==[]
    # and the other will have backward==[] and forward==[[21, {}, set()]]
    for c in self.config.channels:
      self.assertEqual(c.backward, [])
      self.assertIn(c.forward, [[[21, {}, set()]], []])
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
		<goroutine>
			<k> $unit </k>
			<sigma>
				<HB> .Map </HB>
				<S> .Set </S>
			</sigma>
		</goroutine>
	</T>
	<W> .Map </W>
	<C>
		<chan>
			<ref> 2 </ref>
			<type> int </type>
			<forward> ListItem ( ListItem ( 21 ) ListItem ( .Map ) ListItem ( .Set ) ) </forward>
			<backward> .List </backward>
		</chan>
		<chan>
			<ref> 1 </ref>
			<type> int </type>
			<forward> .List </forward>
			<backward> .List </backward>
		</chan>
	</C>
</generatedTop>
''',
              "mmgo-dw" : '''
<generatedTop>
	<T>
		<goroutine>
			<k> 42 </k>
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
	<W> .Map </W>
	<C>
		<chan>
			<ref> 2 </ref>
			<type> int </type>
			<forward> ListItem ( ListItem ( 21 ) ListItem ( .Map ) ListItem ( .Set ) ) </forward>
			<backward> .List </backward>
		</chan>
		<chan>
			<ref> 1 </ref>
			<type> int </type>
			<forward> .List </forward>
			<backward> .List </backward>
		</chan>
	</C>
</generatedTop>
'''}
  test = __file__[0:-2] + 'mmgo'
  semantics = "mmgo-sc"; myunittest.myunittest.check(semantics, test, config[semantics]) 
  semantics = "mmgo-dw"; myunittest.myunittest.check(semantics, test, config[semantics])
