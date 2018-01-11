#! /usr/bin/env python3
# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import sys
import xml.etree.ElementTree as et

import k2py

class Configuration:
  '''
  Channels:

  Channels are created dynamically.
  There is no guaranteed that the reference number will remain the same
  from one test run to the next.
  Tests should not count on the channel's reference number, or even on
  the order of channel creation.
  '''
  def __init__(self, goroutines=[], channels=[], w=[]):
    self.goroutines = goroutines
    self.channels = channels
    self.w = w

  def __str__(self):
    string = "goroutines='%s'" % self.goroutines
    string += ", channels='%s'" % self.channels
    string += ", w='%s'" % self.w
    return string

  def __repr__(self):
    return self.__str__()

class GoRoutine:
  def __init__(self, k="", sigma={"hb" : {}, "s" : set()}):
    self.k = k
    self.sigma = sigma

  def __str__(self):
    string = "k='%s'" % self.k
    string += ", sigma='%s'" % self.sigma
    return string

  def __repr__(self):
    return self.__str__()

class GoChannel:
  def __init__(self, ref=-1, type=None, forward=[], backward=[]):
    self.ref = ref
    self.type = type
    self.forward = forward
    self.backward = backward

  def __str__(self):
    string = "ref='%s'" % self.ref
    string += ", type='%s'" % self.type
    string += ", forward='%s'" % self.forward
    string += ", backward='%s'" % self.backward
    return string

  def __repr__(self):
    return self.__str__()

    
def xml2py(config, debug=False):
  tree = et.fromstring(config)
  # Write events
  el = tree.find('W')
  w = k2py.translate(el.text)
  if debug: print('W'); print(w)
  # Channels
  el = tree.find('C')
  channels = []
  for ch in el.getchildren():
    params = []
    for attr in ch.getchildren():
      params.append("%s = %s" % (attr.tag, k2py.translate(attr.text)))
    string = "GoChannel(" + ", ".join(params) + ")"
    channels.append(eval(string))
    if debug:
      print('Channel')
      print(go_chans[-1].ref); print(go_chan.type);
      print(go_chans[-1].forward); print(go_chan.backward)
  # GoRoutines
  el = tree.find('T')
  goroutines = []
  for gr in el.getchildren():
    params = []
    for attr in gr.getchildren():
      if attr.tag == 'k':
        params.append("%s = '%s'" % (attr.tag, attr.text.strip()))
      elif attr.tag == 'sigma':
        sigma_params = []
        for ch_attr in attr.getchildren():
          sigma_params.append("'%s' : %s" % (ch_attr.tag.lower(),
                                      k2py.translate(ch_attr.text)))
        params.append("%s = {%s}" % (attr.tag, ", ".join(sigma_params)))
    string = "GoRoutine(" + ", ".join(params) + ")"
    goroutines.append(eval(string))
    if debug:
      print("GoRoutine")
      print(goroutines[-1].k)
      print(goroutines[-1].sigma['hb'])
      print(goroutines[-1].sigma['s'])
  return Configuration(goroutines=goroutines, channels=channels, w=w)


def main():
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
  config = xml2py(config['mmgo-dw'])
  print(config)
  return 0

if __name__ == "__main__":
  sys.exit(main())
