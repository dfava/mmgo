// Copyright (C) 2017 Daniel Fava. All Rights Reserved.
require "mmgo-syntax.k"
require "mmgo-common.k"

module MMGO-LOCAL
  imports MMGO-SYNTAX
  imports MMGO-COMMON

 rule if true then E else _ => E
  rule if false then _ else E => E

  rule let Z:Id = V:Val in T:Term => T[V / Z]  // Using built in substitution
  /*@ Because $x is an identifier that cannot appear in a program, 
      we can use it in a let contruct in order to implement sequential comp. */
  syntax Id ::= "$x"  [latex(\_)]
  /*@ A dummy return for expressions that don't return anything */
  syntax Val ::= "$unit"
  /*@ Seq. comp. defined with let construct */
  rule T1:Exp ; T2:Term => let $x = T1 in T2  [macro] // can be defined either
       	      		       	       	      // as [macro] or as [structural]
  rule {} => .	[structural]
  rule {T} => T	[structural]
endmodule
