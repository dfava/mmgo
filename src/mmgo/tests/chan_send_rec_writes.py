# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import myunittest

class Common(myunittest.TestCase):
  def test_k(self):
    self.assertEqual(len(self.config.goroutines), 2)
    for gr in self.config.goroutines:
      self.assertEqual(gr.k, "$unit")

  def test_c_forwardq(self):
    self.assertEqual(len(self.config.channels), 1)
    self.assertEqual(self.config.channels[0].forward, [])
    pass

  def test_c_backwardq(self):
    self.assertEqual(len(self.config.channels), 1)
    self.assertEqual(self.config.channels[0].backward, [])
    pass

class Sc(Common):
  def test_w(self):
    self.assertEqual(self.config.w['y'], 42)
    self.assertIn(self.config.w['x'], [16, 26])
    pass

class Dw(Common):
  def test_hb(self):
    #print(self.config.w)
    #print(self.config.goroutines)
    # For y, the initial value of 0 must be in both thread's happens before,
    # but the write of 42 must be in in only one of the threads
    # TODO

    # For x, the initial value of 0 as well as the write of 1 and of 2
    # must be in both thread's happens before,
    # but the write of 16 must be in one of the thread's hb and not the other,
    # same for the write of 26
    # TODO
    pass

  def test_shadowed(self):
    # TODO: implement
    pass

  def test_w(self):
    ordered_events = {}
    for var in self.config.w.keys():
      ordered_events[var] = sorted(self.config.w[var].items())
    # Check that y was first 0 and then 42
    self.assertEqual(ordered_events['y'][0][1], 0)
    self.assertEqual(ordered_events['y'][1][1], 42)
    # Check that x was first 0 and the it finished execution at either 16 or 26
    self.assertEqual(ordered_events['x'][0][1], 0)
    self.assertIn(ordered_events['x'][-1][1], [16, 26])
    pass


if __name__ == "__main__":
  config = { "mmgo-sc" : '''<generatedTop>
  <T>
    <goroutine>
      <k> $unit </k>
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
  <W> x |-> 16 y |-> 42 </W>
  <C>
    <chan>
      <ref> 1 </ref>
      <type> int </type>
      <forward> .List </forward>
      <backward> .List </backward>
    </chan>
  </C>
</generatedTop>''',
      "mmgo-dw" : '''<generatedTop>
  <T>
    <goroutine>
      <k> $unit </k>
      <sigma>
        <HB> x |-> ( SetItem ( 2 ) SetItem ( 7 ) SetItem ( 9 ) SetItem ( 12 ) ) y |-> ( SetItem ( 3 ) SetItem ( 13 ) ) </HB>
        <S> SetItem ( 2 ) SetItem ( 3 ) SetItem ( 7 ) SetItem ( 9 ) </S>
      </sigma>
    </goroutine>
    <goroutine>
      <k> $unit </k>
      <sigma>
        <HB> x |-> ( SetItem ( 2 ) SetItem ( 7 ) SetItem ( 9 ) SetItem ( 11 ) ) y |-> SetItem ( 3 ) </HB>
        <S> SetItem ( 2 ) SetItem ( 7 ) SetItem ( 9 ) </S>
      </sigma>
    </goroutine>
  </T>
  <W> x |-> ( 9 |-> 2 2 |-> 0 11 |-> 26 12 |-> 16 7 |-> 1 ) y |-> ( 13 |-> 42 3 |-> 0 ) </W>
  <C>
    <chan>
      <ref> 5 </ref>
      <type> int </type>
      <forward> .List </forward>
      <backward> .List </backward>
    </chan>
  </C>
</generatedTop>''' }
  test = __file__[0:-2] + 'mmgo'
  semantics = "mmgo-sc"; myunittest.myunittest.check(semantics, test, config[semantics]) 
  semantics = "mmgo-dw"; myunittest.myunittest.check(semantics, test, config[semantics]) 
