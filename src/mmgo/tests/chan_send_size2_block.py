# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import re
import myunittest

class Common(myunittest.TestCase):
  def test_k(self):
    self.assertEqual(len(self.config.goroutines), 1)
    m = re.match("channel \( .* \) <- 6", self.config.goroutines[0].k)
    self.assertNotEqual(m, None)
    pass

  def test_c_forwardq(self):
    self.assertEqual(self.config.channels[0].forward, 
        [[17, {}, set()], [42, {}, set()]])
    pass

  def test_c_backwardq(self):
    self.assertEqual(self.config.channels[0].backward, [])
    pass

if __name__ == "__main__":
  config = { "mmgo-sc" : '''
<generatedTop>
  <T>
    <goroutine>
      <k> channel ( 2 ) &lt;- 6 </k>
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
      <forward> ListItem ( ListItem ( 17 ) ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( 42 ) ListItem ( .Map ) ListItem ( .Set ) ) </forward>
      <backward> .List </backward>
    </chan>
  </C>
</generatedTop>''',
              "mmgo-dw" : '''
<generatedTop>
  <T>
    <goroutine>
      <k> channel ( 2 ) &lt;- 6 </k>
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
      <forward> ListItem ( ListItem ( 17 ) ListItem ( .Map ) ListItem ( .Set ) ) ListItem ( ListItem ( 42 ) ListItem ( .Map ) ListItem ( .Set ) ) </forward>
      <backward> .List </backward>
    </chan>
  </C>
</generatedTop>''' }
  test = __file__[0:-2] + 'mmgo'
  semantics = "mmgo-sc"; myunittest.myunittest.check(semantics, test, config[semantics]) 
  semantics = "mmgo-dw"; myunittest.myunittest.check(semantics, test, config[semantics])
