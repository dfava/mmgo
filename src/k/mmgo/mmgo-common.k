// Copyright (C) 2017 Daniel Fava. All Rights Reserved.
require "substitution.k"
require "mmgo-syntax.k"

module MMGO-COMMON
  imports MMGO-SYNTAX
  imports SUBSTITUTION

  syntax KVariable ::= Id // For some reason, KVariable must be in this module,
  	 	          // versus in the syntax module

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
  configuration <T color="yellow">
                  <goroutine multiplicity="*" color="blue">
                    <k color="green"> $PGM:Pgm </k>
		    <sigma color="red">
		      <HB color="Orange">
                        .Map // N:Int<Var:Id> implemented as a
			                      // map of Var:Id to Set of N:Int
                      </HB>
		      <S color="Orchid"> .Set </S>// N:Int, implemented as a set
		                                  // of Int (both in dw and drw)
		    </sigma>
		  </goroutine>
		</T>
		<W color="Aquamarine">
                  .Map // The map is interpreted differently depending on the
		  // memory model:
		  // 1) mmgo-sc (sequential consistent or strong model
		  //    its a map from variable to values
		  // 2) mmgo-dw (delayed writes)
		  //    in dw it corresponds to N:Int<Var:Id, Value:Val>,
		  //    which is implemented as map of Var:Id to a Map of
		  //    N:Int to Val.
                </W>
		<C> // Channels
		  <chan multiplicity="*">
		    <ref> . </ref>
		    <type> . </type>
		    <closed> . </closed>
		    <forward> .List </forward>
		    <backward> .List </backward>
		  </chan>
		</C>

  /*@ This rule requires variables to be declared at most once. */
  rule <k> int (Z:Id,Zs:Globals => Zs);_ </k>
       <W> WMap:Map => WMap[ Z <- 0 ] </W>
       requires notBool(Z in keys(WMap)) // no repeated declaration

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

  /*@ A new goroutine inherits $\sigma$ from its ``parent.''
      The $\$unit$ is a return value returned when the goroutine is
      \emph{started}.
      That value is ignored; its sole purpose is to allow execution to continue.
      For example \texttt{go B; T}, the semicolon is sugar for
      \texttt{let \_ = go B in T}.  In order for this rule to apply,
      \texttt{go B} needs to produce a value.  We use $\$unit$ because it is a 
      value that cannot appear in a mmgo program text.*/
  rule <goroutine> <k> go B:Block => $unit ... </k> <sigma>S</sigma> </goroutine>
       (.Bag => <goroutine> <k> B </k> <sigma> S </sigma> </goroutine>)

endmodule
