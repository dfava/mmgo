# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import myunittest

class Common(myunittest.TestCase):
  def test_k(self):
    self.assertEqual(len(self.config.goroutines), 1)
    self.assertEqual(self.config.goroutines[0].k, "1")
    pass

class Dw(Common):
  def test_hb(self):
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
  </T>
  <W> x |-> 0 y |-> 0 </W>
  <C> .ChanCellBag </C>
</generatedTop>''',
              "mmgo-dw" : '''
<generatedTop>
  <T>
    <goroutine>
      <k> 1 </k>
      <sigma>
        <HB> x |-> SetItem ( 2 ) y |-> SetItem ( 3 ) </HB>
        <S> .Set </S>
      </sigma>
    </goroutine>
  </T>
  <W> x |-> ( 2 |-> 0 ) y |-> ( 3 |-> 0 ) </W>
  <C> .ChanCellBag </C>
</generatedTop>''' }
  test = __file__[0:-2] + 'mmgo'
  semantics = "mmgo-sc"; myunittest.myunittest.check(semantics, test, config[semantics]) 
  semantics = "mmgo-dw"; myunittest.myunittest.check(semantics, test, config[semantics])
