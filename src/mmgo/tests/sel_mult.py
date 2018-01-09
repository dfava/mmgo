# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import myunittest
from mmgo import mmgo

# let c1 = make(chan int, 1) in   SelBranchtatus=En 
# let c2 = make(chan int, 1) in   SelBranchtatus=En
# let c3 = make(chan int, 1) in   SelBranchtatus=Empty
# let c4 = make(chan int, 1) in   SelBranchtatus=Full
# let c5 = make(chan int, 1) in   SelBranchtatus=En

class Common(myunittest.TestCase):
  def test_k(self):
    self.assertEqual(len(self.config.goroutines), 1)
    self.assertIn(self.config.goroutines[0].k, ["42", "21", "13"])
    pass

if __name__ == "__main__":
  config = { "mmgo-sc" : '''
''',
              "mmgo-dw" : '''
'''}
  test = __file__[0:-2] + 'mmgo'
  semantics = "mmgo-sc"; myunittest.myunittest.check(semantics, test, config[semantics]) 
  semantics = "mmgo-dw"; myunittest.myunittest.check(semantics, test, config[semantics])
