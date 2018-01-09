# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import myunittest

class Common(myunittest.TestCase):
    pass

class Dw(Common):
  def test_w(self):
    # Make sure every var is initialized to 0
    self.assertEqual(list(self.config.w['x'].items())[0][1], 0)
    self.assertEqual(list(self.config.w['y'].items())[0][1], 0)
    self.assertEqual(list(self.config.w['z'].items())[0][1], 0)
    pass


  def test_hb(self):
    # Make sure declared variables are in the happened before set
    hb_vars = self.config.goroutines[0].sigma['hb'].keys()
    self.assertIn('x', hb_vars)
    self.assertIn('y', hb_vars)
    self.assertIn('z', hb_vars)
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
  <W> x |-> 0 z |-> 0 y |-> 0 </W>
  <C> .ChanCellBag </C>
</generatedTop>''',
              "mmgo-dw" : '''
<generatedTop>
  <T>
    <goroutine>
      <k> 3 </k>
      <sigma>
        <HB> x |-> SetItem ( 2 ) z |-> SetItem ( 4 ) y |-> SetItem ( 5 ) </HB>
        <S> .Set </S>
      </sigma>
    </goroutine>
  </T>
  <W> x |-> ( 2 |-> 0 ) z |-> ( 4 |-> 0 ) y |-> ( 5 |-> 0 ) </W>
  <C> .ChanCellBag </C>
</generatedTop>''' }
  test = __file__[0:-2] + 'mmgo'
  semantics = "mmgo-sc"; myunittest.myunittest.check(semantics, test, config[semantics]) 
  semantics = "mmgo-dw"; myunittest.myunittest.check(semantics, test, config[semantics])
