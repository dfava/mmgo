// Copyright (C) 2017 Daniel Fava. All Rights Reserved.
require "../mmgo/mmgo-syntax.k"
require "../mmgo/mmgo-common.k"

module MMGO-SMEM
  imports MMGO-SYNTAX
  imports MMGO-COMMON

  syntax Map ::= mergeHbAux(Map,Map,K,K)
               | mergeHbAux2(K,K,K,K,K)
               | mergeHbAux3(K,K,K,K)
  rule mergeHB(M1:Map, (Key|->Val) M2:Map) => mergeHB(M1 (Key|->Val), M2:Map)
       requires notBool( Key in_keys ( M1 ))  [anywhere, structural]
  rule mergeHB(M1:Map, (Key |-> Val:K) M2:Map) => mergeHbAux(M1, M2, Key, Val)
       requires Key in_keys ( M1 )            [anywhere, structural]
  rule mergeHbAux(M1,M2,I,V) => mergeHbAux2(M1,M2,I,(M1:Map)[I:Id],V) [anywhere, structural]
  rule mergeHbAux2(M1,M2,I,V1,V2) => mergeHbAux3(M1,M2,I,V1:Set V2) [anywhere, structural]
  rule mergeHbAux3(M1,M2,I,V1) => mergeHB(M1:Map[I:Id <- V1:Set],M2) [anywhere, structural]


  /*@ Traverse through the globals and performs the necessary initialization
      according to the delayed-writes semantic.
      At the start of execution, the global variables are initialized by
      being placed at <W> with a write event of value zero.
      A goroutine is created and the write events of 0 to the global variables
      are recorded in the goroutine's <HB>.
  */
  //rule int .Globals; T => T      [structural]
  syntax VarDec ::= auxInit(K,Set)
  rule <k> auxInit(Z:Id =>
             choice(S -Set SetItem(Z)), S:Set => S -Set SetItem(Z)) ; T </k>
       <HB>
         HMap:Map => HMap[ Z <- SetItem(!N:Int) ]
       </HB>
       <W> ... Z |-> (0 => (!N:Int |-> 0)) ... </W>
       requires size(S) >Int 1
  rule <k> auxInit(Z:Id, S:Set) ; T => T </k>
       <HB>
         HMap:Map => HMap[ Z <- SetItem(!N:Int) ]
       </HB>
       <W> ... Z |-> (0 => (!N:Int |-> 0)) ... </W>
       requires size(S) ==Int 1
  rule <k> (int .Globals => auxInit(choice(WMap),keys(WMap))) ; T </k>
       <W> WMap:Map </W>

       
  /*@ Write rule */
  rule <k> Z:Id := V:Val => $unit ... </k>
       <S> Ss => ( Ss Sh ) </S> // Add to shadow set
       <HB>
         ... Z |-> ( Sh => SetItem(!N:Int) Sh ) ... // Add to happens before
       </HB>
       <W> ... Z |-> ( Mw => Mw[!N:Int <- V] ) ... </W> // Add to global writes

  /*@ Read rule */
  // (Mw[Z])[ (choice(keys((Mw[Z])) -Set Ss)) ]
  rule <k> load Z:Id => loadAux(Mw,Ss,Z) ... </k>
       <S> Ss:Set </S>
       <W> Mw:Map </W>
  syntax K ::= loadAux(Map,Set,Id)
         | loadAux2(K,Set)
       | loadAux3(K,K,Set)
       | loadAux4(K,K)
       | loadAux5(K,K)
  rule loadAux(M,S,I)     => loadAux2(M[I],S)     [structural]
  rule loadAux2(M2,S)     => loadAux3(keys(M2),M2,S)    [structural]
  rule loadAux3(S2,M2,S)  => loadAux4(S2:Set -Set S, M2)  [structural]
  rule loadAux4(S3,M2)    => loadAux5(choice(S3:Set),M2)  [structural]
  rule loadAux5(K,M2)     => (M2:Map)[K:Int]      [structural]
endmodule
