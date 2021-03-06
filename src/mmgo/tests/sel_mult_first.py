# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import myunittest
from mmgo import mmgo


class Common(myunittest.TestCase):
  def test_k(self):
    self.assertEqual(len(self.config.goroutines), 1)
    self.assertEqual(self.config.goroutines[0].k, "42")
    #self.assertEqual(self.config.goroutines[0].k, "let r = <- channel ( 1 ) in r")
    pass

if __name__ == "__main__":
  config = { "mmgo-sc" : '''
''',
              "mmgo-dw" : '''
'''}
  test = __file__[0:-2] + 'mmgo'
  semantics = "mmgo-sc"; myunittest.myunittest.check(semantics, test, config[semantics]) 
  semantics = "mmgo-dw"; myunittest.myunittest.check(semantics, test, config[semantics])
