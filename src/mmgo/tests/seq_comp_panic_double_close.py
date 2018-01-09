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
    self.assertEqual(self.config.channels[0].forward, [['$eot', {}, set()]])
    pass

  def test_c_backwardq(self):
    self.assertEqual(self.config.channels[0].backward, 
        [[{}, set()], [{}, set()]])
    pass
