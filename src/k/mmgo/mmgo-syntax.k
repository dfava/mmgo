// Copyright (C) 2017 Daniel Fava. All Rights Reserved.
module MMGO-SYNTAX
  imports DOMAINS

  syntax Type ::= "int" | "bool"
  syntax AExp ::= Int | Id
                | "(" AExp ")"  [brackets]
                > left:
                  AExp "*" AExp [strict, left]
                | AExp "/" AExp [strict, left]
                > left:
                  AExp "+" AExp [strict, left]
                | AExp "-" AExp [strict, left]
  syntax TVal ::= Bool | Int
  syntax Val ::= TVal | Id
  syntax Exp ::= Val | AExp
              // on "if" there is no need for strict(1) since arg 1 is Val
                | "if" Val "then" Term "else" Term  [klabel(If)]
                | "load" Id
                | Id ":=" Val
                | "go" Block        [klabel(Go)]
                | "make" "(" "chan" Type "," Int ")"
                | Val "<-" Val      [klabel(SExp)] // Channel send expression
                | "<-" Val          [klabel(RExp)] // Channel receive expression
                | "close" "(" Val ")"
                | "sel" "{" GBranch "}"
                | "sel" "{" "}" // This is the same as "halt"

  // Guarded expressions
  syntax LetChan ::= "let" Id "=" Val "<-" Val "in" Term  [binder]
                   | "let" Id "="     "<-" Val "in" Term  [binder]
  // We require/expect (in mmgo-select.k) that "default" is always the last branch
  syntax LetDef ::=  "let" Id "=" "default" "in" Term     [binder]
  syntax GBranch ::= "{" LetChan "}"
                   | "{" LetDef  "}"
                   | "{" LetChan "}" GBranch

  syntax Block ::= "{" "}"
                 | "{" Term "}"
  syntax Term ::= Exp
                | Exp ";"
                | Block
                // on "let" we set strict(2) so Exp is eval'ed first
                > "let" Id "=" Exp "in" Term    [binder, strict(2)]
                > Term ";" Term               [klabel(Semicolon),
                                               right, seqstrict]

  /*@ A program is a (posibly empty) list of globals followed by a term */
  syntax Globals ::= List{Id,","}
  syntax BoolDec ::= "bool" Globals
  syntax IntDec ::= "int" Globals
  syntax VarDec ::= BoolDec | IntDec
  syntax Pgm ::= VarDec ";" Term
               | Term
  syntax KResult ::= Val
endmodule
