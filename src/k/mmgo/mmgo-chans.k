// Copyright (C) 2017 Daniel Fava. All Rights Reserved.
require "mmgo-syntax.k"
require "mmgo-common.k"

module MMGO-CHANS
  imports MMGO-SYNTAX
  imports MMGO-COMMON

  syntax Val ::= "channel" "(" Int ")" | "$eot"

  syntax Map ::= mergeHB(Map, Map)
  rule mergeHB(H1:Map, .Map) => H1:Map [anywhere, structural]

  syntax Bool ::= "EotInFQ" "(" List ")"
  syntax Bool ::= "IsEot" "(" List ")"
  rule EotInFQ(.List) => false                      [anywhere, structural]
  rule EotInFQ(ListItem(H:List) _:List) => IsEot(H) [anywhere, structural]
  rule IsEot(ListItem(H) _:List) => H==K $eot       [anywhere, structural]


  /*@ Channel creation.
      Channels are typed and have finite (non-negative) buffers.
      A zero sized channel is a synchronous channel.
  */
  syntax K ::= makeAux(Int,Int)
  // Note: It is OK for this rule not to be "atomic"
  // Even though there will be intermediate states where the channel is not
  // fully created yet (as seen in the makeAux), no other reduction can observe
  // this intermediate state because no one will have the channel reference
  // until the auxiliary reduction rules have completed.
  rule <k> make (chan T:Type, Size:Int ) => makeAux(!N:Int, Size) ... </k>
       <C> ... .Bag => <chan>
          <ref> !N:Int </ref>
          <type> T </type>
          <forward> .List </forward>
          <backward> .List </backward>
          </chan>
       </C>
       requires Size >=Int 0
  /*@ Place dummy elements on the backward queue of a newly created channel */
  rule <k> makeAux(Ref,0) => channel(Ref) ... </k>  [structural]
  rule <k> makeAux(Ref,Cnt) => makeAux(Ref,Cnt -Int 1) ... </k>
        <chan>
          <ref> Ref </ref>
          <type> _ </type>
          <forward> _ </forward>
          <backward> ... .List => ListItem( ListItem( .Map )
            ListItem( .Set ) ) </backward>
        </chan>
       requires Cnt >Int 0  [structural]


  /*@ Sending on a channel
      A channel is modeled as a queue.
      Q[0] is the first item placed in the channel which hasn't been read yet.
      Q[-1] is the last item placed in the channel.

      Channels are typed, but we don't check the type of the channel against the 
      value being sent. We use the type of the channel when reading from a
      closed channel, in which case we return the zero value for the given 
      channel type.
  */
  rule <goroutine>
        <k> channel(Ref:Int) <- V:Val => $unit ... </k>
        <sigma>
          <HB> HMap:Map => mergeHB(HMap, HMapDP) </HB>
          <S>  SSet:Set => SSet SSetDP </S>
        </sigma>
        <select> _ </select>
        <id> _ </id>
      </goroutine>
      <chan>
        <ref> Ref </ref>
        <type> _ </type>
        <forward> FQ:List => ListItem( ListItem(V)
          ListItem(HMap)
          ListItem(SSet) ) FQ </forward>
        <backward> _:List (ListItem( ListItem(HMapDP)
                              ListItem(SSetDP) ) => .List) </backward>
      </chan>
      requires EotInFQ( FQ ) ==Bool false
  rule <goroutine>
        <k> channel(Ref:Int) <- V:Val => $unit ... </k>
        <sigma>
          <HB> HMap:Map => mergeHB(HMap, HMapDP) </HB>
          <S>  SSet:Set => SSet SSetDP </S>
        </sigma>
        <select> _ </select>
        <id> _ </id>
      </goroutine>
      <chan>
        <ref> Ref </ref>
        <type> _ </type>
        <forward> FQ:List => ListItem( ListItem(V)
          ListItem(HMap)
          ListItem(SSet) ) FQ </forward>
        <backward> (ListItem( ListItem(HMapDP)
                              ListItem(SSetDP) ) => .List) </backward>
      </chan>
      requires EotInFQ( FQ ) ==Bool false


  /*@ Attempt to send on a closed channel:
      A send of a closed channel must not reduce, that is our version of
      a panic.  As a visual aid when running actual programs, we'll reduce
      to "$panic".
  */
  syntax K ::= "$panic"
  rule <k> channel(Ref:Int) <- V:Val => $panic ... </k>
       <chan>
         <ref> Ref </ref>
        <type> _ </type>
        <forward> FQ:List </forward>
        <backward> _ </backward>
       </chan>
      requires EotInFQ( FQ )



  /*@ Receiving on a channel */
  rule <goroutine>
        <k> <- channel(Ref:Int) => V ... </k>
        <sigma>
          <HB> HMap:Map => mergeHB(HMap, HMapDP) </HB>
          <S>  SSet:Set => SSet SSetDP </S>
        </sigma> // Change from Sigma to (Sigma + Sigma'')
        <select> _ </select>
        <id> _ </id>
      </goroutine>
      <chan>
        <ref> Ref </ref>
        <type> _ </type>
        <forward> ListItem( ListItem(V)
                    ListItem(HMapDP)
                    ListItem(SSetDP) ) => .List </forward>
        <backward> BQ:List => ListItem( ListItem(HMap)
                              ListItem(SSet) ) BQ </backward>
      </chan>
      requires notBool( V ==K $eot )
  rule <goroutine>
        <k> <- channel(Ref:Int) => V ... </k>
        <sigma>
          <HB> HMap:Map => mergeHB(HMap, HMapDP) </HB>
          <S>  SSet:Set => SSet SSetDP </S>
        </sigma> // Change from Sigma to (Sigma + Sigma'')
        <select> _ </select>
        <id> _ </id>
      </goroutine>
      <chan>
        <ref> Ref </ref>
        <type> _ </type>
        <forward> _:List (ListItem( ListItem(V)
                          ListItem(HMapDP)
                          ListItem(SSetDP) ) => .List) </forward>
        <backward> BQ:List => ListItem( ListItem(HMap)
                                        ListItem(SSet) ) BQ </backward>
      </chan>
      requires notBool( V ==K $eot )


  /*@ Receiving on a closed channel returns the zero element
      for the type of the channel when the channel is empty. */
  syntax K ::= zero(Type)
  rule <k> zero(bool) => false </k>
  rule <k> zero(int) => 0 </k>
  rule <goroutine>
        <k> <- channel(Ref:Int) => zero(T) ... </k>
        <sigma>
          <HB> HMap:Map => mergeHB(HMap, HMapDP) </HB>
          <S>  SSet:Set => SSet SSetDP </S>
        </sigma> // Change from Sigma to (Sigma + Sigma'')
        <select> _ </select>
        <id> _ </id>
      </goroutine>
      <chan>
        <ref> Ref </ref>
        <type> T:Type </type>
        <forward>
          ListItem( ListItem($eot) ListItem(HMapDP) ListItem(SSetDP) )
        </forward>
        <backward> _ </backward>
      </chan>



  /*@ Synchronous send/receive */
  rule <goroutine>
        <k> channel(Ref:Int) <- V:Val => $unit ... </k>
        <sigma>
          <HB> HMapS:Map => mergeHB( HMapS, HMapR ) </HB>
          <S>  SSetS:Set => SSetS SSetR </S>
        </sigma>
        <select> _ </select>
        <id> _ </id>
      </goroutine>
      <goroutine>
        <k> <- channel(Ref:Int) => V ... </k>
        <sigma>
          <HB> HMapR:Map => mergeHB( HMapS, HMapR ) </HB>
          <S>  SSetR:Set => SSetS SSetR </S>
        </sigma>
        <select> _ </select>
        <id> _ </id>
      </goroutine>
        <chan>
          <ref> Ref </ref>
          <type> _ </type>
          <forward> .List </forward>
          <backward> .List </backward>
        </chan>


  /*@ Closing a channel
      The closing happens immediately regardless of whether the channel is full.
  */
  rule <goroutine>
        <k> close( channel(Ref:Int) ) => $unit ... </k>
        <sigma>
          <HB> HMap:Map </HB>
          <S>  SSet:Set </S>
        </sigma>
        <select> _ </select>
        <id> _ </id>
      </goroutine>
        <chan>
          <ref> Ref </ref>
          <type> _ </type>
          <forward> FQ:List => ListItem( ListItem($eot)
                                          ListItem(HMap)
                                          ListItem(SSet) ) FQ </forward>
          <backward> _ </backward>
        </chan>
      requires EotInFQ( FQ ) ==Bool false
  rule <k> close( channel(Ref:Int) ) => $panic ... </k>
        <chan>
          <ref> Ref </ref>
          <type> _ </type>
          <forward> FQ:List </forward>
          <backward> _ </backward>
        </chan>
      requires EotInFQ( FQ )

endmodule
