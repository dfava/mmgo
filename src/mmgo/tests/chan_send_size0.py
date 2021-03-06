# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import re
import myunittest

class Common(myunittest.TestCase):
  def test_k(self):
    self.assertEqual(len(self.config.goroutines), 1)
    m = re.match("channel \( .* \) <- 42", self.config.goroutines[0].k)
    self.assertNotEqual(m, None)
    pass

if __name__ == "__main__":
  config = { "mmgo-sc" : '''
<generatedTop>
  <T>
    <goroutine>
      <k> channel ( 2 ) &lt;- 42 </k>
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
      <k> channel ( 2 ) &lt;- 42 </k>
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
      <forward> .List </forward>
      <backward> .List </backward>
    </chan>
  </C>
</generatedTop>
'''}
  test = __file__[0:-2] + 'mmgo'
  semantics = "mmgo-sc"; myunittest.myunittest.check(semantics, test, config[semantics]) 
  semantics = "mmgo-dw"; myunittest.myunittest.check(semantics, test, config[semantics])
