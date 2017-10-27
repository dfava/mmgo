#! /usr/bin/env python3
# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import unittest
from pyparsing import *

def get_grammar(debug=False):
	grammar = Forward()
	integer = Word( nums ).setParseAction(lambda s,l,t: int(t[0]))
	identifier = Word( alphas )
	lp = Suppress(Literal("("))
	rp = Suppress(Literal(")"))
	ListItem  = Literal("ListItem") + lp + grammar + rp
	ListItem  = ListItem.setParseAction(lambda s,l,t: [t[1:len(t)]])
	ListEmpty = Literal(".List")
	ListEmpty = ListEmpty.setParseAction(lambda s,l,t: [])
	List      = (ListEmpty | OneOrMore(ListItem))
	List			= List.setParseAction(lambda s,l,t: [[i for sublist in t for i in sublist]])

	SetItem   = Literal("SetItem") + lp + grammar + rp
	SetItem		= SetItem.setParseAction(lambda s,l,t: set(t[1:len(t)]))
	SetEmpty  = Literal(".Set")
	SetEmpty  = SetEmpty.setParseAction(lambda s,l,t: set())
	Set       = (SetEmpty | OneOrMore(SetItem))
	Set       = Set.setParseAction(lambda s,l,t: {i for Set in t for i in Set})

	MapEmpty  = Literal(".Map")
	MapEmpty  = MapEmpty.setParseAction(lambda s,l,t: {})
	MapArrow  = Literal("|->")
	MapKey    = integer | identifier
	MapItem   = MapKey + MapArrow + grammar
	MapItem   = MapItem.setParseAction(lambda s,l,t: {t[0]:t[2]})
	Map       = (MapEmpty | OneOrMore(MapItem))
	Map       = Map.setParseAction(lambda s, l, t: {k: v for d in t for k, v in d.items()})
	grammar << (List | Set | Map | integer | identifier | lp + grammar + rp )
	return grammar

def translate(kstr, grammar=None):
	if grammar == None:
		grammar = get_grammar()
	return grammar.parseString(kstr).asList()[0]

class test(unittest.TestCase):

	def test_list(self):
		kstr = "ListItem(1)"
		self.assertEqual(translate(kstr), [1])

		kstr = "ListItem(1) ListItem(2)"
		self.assertEqual(translate(kstr), [1, 2])

		kstr = "ListItem(ListItem(ListItem ( ListItem ( 42 ) ListItem ( .Map ) ListItem ( .Set ) )))"
		self.assertEqual(translate(kstr), [[[[42, {}, set()]]]])

		kstr = "ListItem(ListItem ( ListItem ( 42 ) ListItem ( .Map ) ListItem ( .Set ) )))"
		self.assertEqual(translate(kstr), [[[42, {}, set()]]])
		pass

	def test_map(self):
		kstr = "x |-> ( 2 |-> 0 6 |-> 42 10 |-> 0 ) y |-> ( 9 |-> 24 3 |-> 0)"
		self.assertEqual(translate(kstr),
				{'x': {2: 0, 6: 42, 10: 0}, 'y': {9: 24, 3: 0}})
		pass

	def test_set(self):
		kstr = "x |-> ( SetItem ( 2 ) SetItem ( 6 ) SetItem ( 10 ) ) y |-> ( SetItem ( 3 ) SetItem ( 9 ) )"
		self.assertEqual(translate(kstr), {'x' : {2, 6, 10}, 'y' : {3, 9}})
		pass

if __name__ == "__main__":
	unittest.main()
