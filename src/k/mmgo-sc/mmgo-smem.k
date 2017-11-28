// Copyright (C) 2017 Daniel Fava. All Rights Reserved.
require "../mmgo/mmgo-syntax.k"
require "../mmgo/mmgo-common.k"

module MMGO-SMEM
  imports MMGO-SYNTAX
  imports MMGO-COMMON

  /*@ Write rule */
  rule <k> Z:Id := V:Val => $unit ... </k>
       <W> ... Z |-> ( _ => V ) ... </W> // Update global writes

  /*@ Read rule */
  rule <k> load Z:Id => V ... </k>
       <W> ... Z |-> V ... </W>
endmodule
