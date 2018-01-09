# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import myunittest

class Common(myunittest.TestCase):
  def test_k(self):
    self.assertEqual(len(self.config.goroutines), 2)
    self.assertEqual(self.config.goroutines[0].k, "6")
    self.assertEqual(self.config.goroutines[1].k, "5")
    pass

class Dw(Common):
  def test_w(self):
    self.assertEqual(list(self.config.w['x'].items())[0][1], 0)
    self.assertEqual(list(self.config.w['y'].items())[0][1], 0)
    self.assertEqual(list(self.config.w['z'].items())[0][1], 0)
    pass

  def test_hb(self):
    self.assertEqual(len(self.config.goroutines), 2) # 2 goroutines
    for gr in self.config.goroutines:
      self.assertEqual(len(gr.sigma['hb']), 3) # 3 variables
      for var in gr.sigma['hb']:
        self.assertEqual(list(gr.sigma['hb'][var])[0], 
                          list(self.config.w[var].items())[0][0])
    pass


if __name__ == "__main__":
  config = { "mmgo-sc" : '''
<generatedTop>
  <T>
    <goroutine>
      <k> 6 </k>
      <sigma>
        <HB> .Map </HB>
        <S> .Set </S>
      </sigma>
    </goroutine>
    <goroutine>
      <k> 5 </k>
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
      <k> 6 </k>
      <sigma>
        <HB> x |-> SetItem ( 2 ) z |-> SetItem ( 4 ) y |-> SetItem ( 5 ) </HB>
        <S> .Set </S>
      </sigma>
    </goroutine>
    <goroutine>
      <k> 5 </k>
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
