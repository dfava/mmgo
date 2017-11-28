// Copyright (C) 2017 Daniel Fava. All Rights Reserved.
require "mmgo-syntax.k"
require "mmgo-common.k"

module MMGO-CHANS
  imports MMGO-SYNTAX
  imports MMGO-COMMON

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
			 <closed> false </closed>
                         <forward> .List </forward>
		         <backward> .List </backward>
		       </chan>
       </C>
       requires Size >=Int 0
  /*@ Place dummy elements on the backward queue of a newly created channel */
  rule <k> makeAux(Ref,0) => channel(Ref) ... </k>	[structural]
  rule <k> makeAux(Ref,Cnt) => makeAux(Ref,Cnt -Int 1) ... </k>
       <chan>
         <ref> Ref </ref>
	 <type> _ </type>
	 <closed> _ </closed>
	 <forward> _ </forward>
	 <backward> ... .List => ListItem( ListItem( .Map )
					   ListItem( .Set ) ) </backward>
       </chan>
       requires Cnt >Int 0	[structural]

  /*@ Sending on a channel
      A channel is modeled as a queue.
      Q[0] is the first item placed in the channel which hasn't been read yet.
      Q[-1] is the last item placed in the channel.

      Channels are typed, but we don't check the type of the channel against the 
      value being sent.  We use the type of the channel when reading from a
      closed channel, in which case we return the zero value for the given 
      channel type.
  */
  syntax Exp ::= "pend" "(" Int ")"
  rule <goroutine>
         <k> channel(Ref:Int) <- V:Val => pend(Ref) ... </k>
	 <sigma>
	   <HB> HMap </HB>
	   <S> SSet </S>
	 </sigma>
       </goroutine>
       <chan>
         <ref> Ref </ref>
	 <type> _ </type>
	 <closed> false </closed>
	 <forward> FQ:List => ListItem( ListItem(V)
					ListItem(HMap)
					ListItem(SSet) ) FQ </forward>
	 <backward> _ </backward>
       </chan>

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
	 <closed> true </closed>
	 <forward> _ </forward>
	 <backward> _ </backward>
       </chan>


  syntax Map ::= mergeHB(Map, Map)
  rule <HB> mergeHB(H1:Map, .Map) => H1:Map </HB>	[structural]

  /*@ pend rule */
  rule <goroutine>
         <k> pend(Ref:Int) => $unit ... </k>
	 <sigma>
	   <HB>
	     HMap:Map => mergeHB(HMap, HMapDP)
	   </HB>
	   <S> SSet:Set => SSet SSetDP </S>
	 </sigma> // Change from Sigma to (Sigma + Sigma'')
       </goroutine>
       <chan>
         <ref> Ref </ref>
	 <type> _ </type>
	 <closed> _ </closed>
	 <forward> _ </forward>
	 <backward> _:List (ListItem( ListItem(HMapDP)
                              ListItem(SSetDP) ) =>  .List) </backward>
       </chan>
  rule <goroutine>
         <k> pend(Ref:Int) => $unit ... </k>
	 <sigma>
	   <HB>
             HMap:Map => mergeHB(HMap, HMapDP)
           </HB>
	   <S> SSet:Set => SSet SSetDP </S>
	 </sigma> // Change from Sigma to (Sigma + Sigma'')
       </goroutine>
       <chan>
         <ref> Ref </ref>
	 <type> _ </type>
	 <closed> _ </closed>
	 <forward> _ </forward>
	 <backward> (ListItem( ListItem(HMapDP)
                              ListItem(SSetDP) ) =>  .List) </backward>
       </chan>


  /*@ Receiving on a channel */
  rule <goroutine>
         <k> <- channel(Ref:Int) => V ... </k>
	 <sigma>
	   <HB>
             HMap:Map => mergeHB(HMap, HMapDP)
           </HB>
	   <S> SSet:Set => SSet SSetDP </S>
	 </sigma> // Change from Sigma to (Sigma + Sigma'')
       </goroutine>
       <chan>
         <ref> Ref </ref>
	 <type> _ </type>
	 <closed> _ </closed>
	 <forward> ListItem( ListItem(V)
		             ListItem(HMapDP)
                             ListItem(SSetDP) ) => .List </forward>
	 <backward> BQ:List => ListItem( ListItem(HMap)
					 ListItem(SSet) ) BQ </backward>
       </chan>
  rule <goroutine>
         <k> <- channel(Ref:Int) => V ... </k>
	 <sigma>
	   <HB>
             HMap:Map => mergeHB(HMap, HMapDP)
           </HB>
	   <S> SSet:Set => SSet SSetDP </S>
	 </sigma> // Change from Sigma to (Sigma + Sigma'')
       </goroutine>
       <chan>
         <ref> Ref </ref>
	 <type> _ </type>
	 <closed> _ </closed>
	 <forward> _:List (ListItem( ListItem(V)
				     ListItem(HMapDP)
				     ListItem(SSetDP) ) => .List) </forward>
	 <backward> BQ:List => ListItem( ListItem(HMap)
					 ListItem(SSet) ) BQ </backward>
       </chan>


  /*@ Receiving on a closed channel returns the zero element
      for the type of the channel when the channel is empty. */
  syntax K ::= zero(Type)
  rule <k> zero(bool) => false </k>
  rule <k> zero(int) => 0 </k>
  rule <k> <- channel(Ref:Int) => zero(T) ... </k>
       <chan>
         <ref> Ref </ref>
	 <type> T:Type </type>
	 <closed> true </closed>
	 <forward> .List </forward>
	 <backward> _ </backward>
       </chan>

  /*@ Closing a channel
      The closing happens immediately regardless of whether the channel is full.
  */
  rule <k> close( channel(Ref:Int) ) => $unit ... </k>
       <chan>
         <ref> Ref </ref>
	 <type> _ </type>
	 <closed> _ => true </closed>
	 <forward> _ </forward>
	 <backward> _ </backward>
       </chan>

endmodule
