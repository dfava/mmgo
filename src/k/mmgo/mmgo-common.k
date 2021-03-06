// Copyright (C) 2017 Daniel Fava. All Rights Reserved.
require "mmgo-syntax.k"

module MMGO-COMMON
  imports MMGO-SYNTAX

  /*@ A dummy return for expressions that don't return anything */
  syntax Val ::= "$unit"

  syntax Map ::= mergeHB(Map, Map)
  rule mergeHB(H1:Map, .Map) => H1:Map [anywhere, structural]


  /*@ A program starts with a single goroutine which can create new goroutines.
      Thus, a term is a collection of one or more goroutines.

      In the delayed-write memory model, each goroutine has a local state sigma
      which contains:
      \begin{itemize}
        \item the events perceived by the goroutine as having already happened,
              represented by <W>, and
        \item a set called the shadow set, represented by <S>.
      \end{itemize}
      All writes to global variables are recorded in <W>.

      Information about channels are kept inside <C></C>
      Each channel information is kept on its own <chan> tag.
      Each channel gets an integer used to reference it, kept in <ref>
      Channels have a <type>, <size> (aka. capacity), a <forward> and 
      a <backward> queue, modeled here as Lists.
  */
  configuration <mmgo>
                  <T color="yellow">
                    <goroutine multiplicity="*" color="blue">
                      <id> !N:Int </id>
                      <k color="green"> $PGM:Pgm </k>
                      <select>
                        <selBranch multiplicity="*"> . </selBranch>  
                      </select>
                      <sigma color="red">
                        <HB color="Orange">
                          .Map // N:Int<Var:Id> implemented as a map of Var:Id to Set of N:Int
                        </HB>
                        <S color="Orchid">
                          .Set // N:Int, implemented as a set of Int (both in dw and drw)
                        </S>
                      </sigma>
                    </goroutine>
                  </T>
                  <W color="Aquamarine">
                    .Map // The map is interpreted differently depending on the memory model:
                         // 1) mmgo-sc (sequential consistent or strong model
                         //    its a map from variable to values
                         // 2) mmgo-dw (delayed writes)
                         //    in dw it corresponds to N:Int<Var:Id, Value:Val>,
                         //    which is implemented as map of Var:Id to a Map of
                         //    N:Int to Val.
                  </W>
                  <C> // Channels
                    <Chan multiplicity="*">
                    <ref> . </ref>
                    <type> . </type>
                    <forward> .List </forward>
                    <backward> .List </backward>
                  </Chan>
                </C>
              </mmgo>

  /*@ This rule requires variables to be declared at most once. */
  rule <k> int (Z:Id,Zs:Globals => Zs);_ </k>
       <W> WMap:Map => WMap[ Z <- 0 ] </W>
       requires notBool(Z in keys(WMap)) // no repeated declaration
endmodule
