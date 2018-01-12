// Copyright (C) 2017 Daniel Fava. All Rights Reserved.
requires "../mmgo-dw/mmgo.k"
requires "kat.k"

module MMGO-ANALYSIS
  imports STRATEGY
endmodule

module MMGO-KAT
  imports MMGO
  imports KAT

  configuration <kat-mmgo> initSCell(Init) initKatCell initMmgoCell(Init) </kat-mmgo>

  syntax State ::= "{" K "}"


  // ### Define `push` and `pop`
  rule <s> push => push { KCELL } ... </s> <mmgo> <k> KCELL </k> </mmgo>
  rule <s> pop { KCELL } => . ... </s> <mmgo> <k> _ => KCELL </k> </mmgo>


  // ### Define `#transition` and `#normal`
  rule <s> #transition => . ... </s>
  rule <s> #normal     => . ... </s>


  // ### Define `bool?`
  rule <s> bool? [ { true  } ] => #true  ... </s>
  rule <s> bool? [ { false } ] => #false ... </s>

endmodule
