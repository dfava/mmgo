// Copyright (C) 2017 Daniel Fava. All Rights Reserved.
require "substitution.k"
require "mmgo-syntax.k"
require "mmgo-chans.k"

module MMGO-SELECT
  imports SUBSTITUTION
  imports MMGO-SYNTAX
  imports MMGO-CHANS

  syntax Val ::= "default"

  syntax K ::= "selAux" "(" GBranch ")"
  syntax K ::= "selClear"
  rule <k> sel { Bs } => selAux(Bs) ... </k> [structural]

  /*@
   *  Setup the select
   */
  rule <goroutine>
         <k> selAux({BHead:LetDef}) => selAux(.K) ... </k>
         <select> ... .Bag => <selBranch> BHead </selBranch> </select>
         <sigma> _ </sigma>
         <id> _ </id>
       </goroutine> [structural]
  rule <goroutine>
         <k> selAux({BHead:LetChan}) => selAux(.K) ... </k>
         <select> ... .Bag => <selBranch> BHead </selBranch> </select>
         <sigma> _ </sigma>
         <id> _ </id>
       </goroutine> [structural]
  rule <goroutine>
         <k> selAux({BHead:LetChan} BTail:GBranch) => selAux(BTail) ... </k>
         <select> ... .Bag => <selBranch> BHead </selBranch> </select>
         <sigma> _ </sigma>
         <id> _ </id>
       </goroutine> [structural]
  /*@
   *  Tear down the select
   */
  rule <goroutine>
         <k> selClear => .K ... </k>
         <select> S => .Bag </select>
         <sigma> _ </sigma>
         <id> _ </id>
       </goroutine> [structural]


  /*@
   *  Sending on a channel
   */
  rule <goroutine>
         <k> selAux(.K) => selClear ~> T[$unit/Z] ... </k>
         <select>
           ...
           <selBranch> (let Z:Id = channel(Ref:Int) <- V:Val in T:Term):LetChan </selBranch>
           ...
         </select>
         <sigma>
           <HB> HMap:Map => mergeHB(HMap, HMapDP) </HB>
           <S>  SSet:Set => SSet SSetDP </S>
         </sigma>
         <id> _ </id>
       </goroutine>
       <Chan>
         <ref> Ref </ref>
         <type> _ </type>
         <forward> FQ:List => ListItem( ListItem(V)
           ListItem(HMap)
           ListItem(SSet) ) FQ </forward>
         <backward> _:List (ListItem( ListItem(HMapDP) ListItem(SSetDP) ) => .List) </backward>
       </Chan>
       requires EotInFQ( FQ ) ==Bool false
  rule <goroutine>
         <k> selAux(.K) => selClear ~> T[$unit/Z] ... </k>
         <select>
           ...
           <selBranch> (let Z:Id = channel(Ref:Int) <- V:Val in T:Term):LetChan </selBranch>
           ...
         </select>
         <sigma>
           <HB> HMap:Map => mergeHB(HMap, HMapDP) </HB>
           <S>  SSet:Set => SSet SSetDP </S>
         </sigma>
         <id> _ </id>
       </goroutine>
       <Chan>
         <ref> Ref </ref>
         <type> _ </type>
         <forward> FQ:List => ListItem( ListItem(V)
           ListItem(HMap)
           ListItem(SSet) ) FQ </forward>
         <backward> (ListItem( ListItem(HMapDP) ListItem(SSetDP) ) => .List) </backward>
       </Chan>
       requires EotInFQ( FQ ) ==Bool false

  /*@
   *  Receiving on a channel
   */
  rule <goroutine>
         <k> selAux(.K) => selClear ~> T[V/Z] ... </k>
         <select>
           ...
           <selBranch> (let Z:Id = <- channel(Ref:Int) in T:Term):LetChan </selBranch>
           ...
         </select>
         <sigma>
           <HB> HMap:Map => mergeHB(HMap, HMapDP) </HB>
           <S>  SSet:Set => SSet SSetDP </S>
         </sigma>
         <id> _ </id>
       </goroutine>
       <Chan>
         <ref> Ref </ref>
         <type> _ </type>
         <forward> ListItem(ListItem(V)
                            ListItem(HMapDP)
                            ListItem(SSetDP) ) => .List </forward>
         <backward> BQ:List => ListItem( ListItem(HMap) ListItem(SSet) ) BQ </backward>
       </Chan>
       requires notBool( V ==K $eot )
  rule <goroutine>
         <k> selAux(.K) => selClear ~> T[V/Z] ... </k>
         <select>
           ...
           <selBranch> (let Z:Id = <- channel(Ref:Int) in T:Term):LetChan </selBranch>
           ...
         </select>
         <sigma>
           <HB> HMap:Map => mergeHB(HMap, HMapDP) </HB>
           <S>  SSet:Set => SSet SSetDP </S>
         </sigma>
         <id> _ </id>
       </goroutine>
       <Chan>
         <ref> Ref </ref>
         <type> _ </type>
         <forward> _:List (ListItem( ListItem(V)
                           ListItem(HMapDP)
                           ListItem(SSetDP) ) => .List) </forward>
         <backward> BQ:List => ListItem( ListItem(HMap) ListItem(SSet) ) BQ </backward>
       </Chan>
       requires notBool( V ==K $eot )

  /*@
   *  Receiving on a closed channel
   */
  rule <goroutine>
         <k> selAux(.K) => selClear ~> T[zero(ChanType)/Z] ... </k>
         <select>
           ...
           <selBranch> (let Z:Id = <- channel(Ref:Int) in T:Term):LetChan </selBranch>
           ...
         </select>
         <sigma>
           <HB> HMap:Map => mergeHB(HMap, HMapDP) </HB>
           <S>  SSet:Set => SSet SSetDP </S>
         </sigma>
         <id> _ </id>
       </goroutine>
       <Chan>
         <ref> Ref </ref>
         <type> ChanType:Type </type>
         <forward>
           ListItem( ListItem($eot) ListItem(HMapDP) ListItem(SSetDP) )
         </forward>
         <backward> _ </backward>
       </Chan>

  /*@
   *  Synchronous send/receive rules
   */
  rule <goroutine> // Receiver
         <k> selAux(.K) => selClear ~> T[V/Z] ... </k>
         <select>
           ...
           <selBranch> (let Z:Id = <- channel(Ref:Int) in T:Term):LetChan </selBranch>
           ...
         </select>
         <sigma>
           <HB> HMapR:Map => mergeHB( HMapS, HMapR ) </HB>
           <S>  SSetR:Set => SSetS SSetR </S>
         </sigma>
         <id> _ </id>
       </goroutine>
       <goroutine> // Partner sender
         <k> channel(Ref:Int) <- V:Val => $unit </k>
         <sigma>
           <HB> HMapS:Map => mergeHB( HMapS, HMapR ) </HB>
           <S>  SSetS:Set => SSetS SSetR </S>
         </sigma>
         <select>_</select>
         <id> _ </id>
       </goroutine>
       <Chan>
         <ref> Ref </ref>
         <type> _ </type>
         <forward> .List </forward>
         <backward> .List </backward>
       </Chan>
  rule <goroutine> // Sender
         <k> selAux(.K) => selClear ~> T[$unit/Z] ... </k>
         <select>
           ...
           <selBranch> (let Z:Id = channel(Ref:Int) <- V:Val in T:Term):LetChan </selBranch>
           ...
         </select>
         <sigma>
           <HB> HMapS:Map => mergeHB( HMapS, HMapR ) </HB>
           <S>  SSetS:Set => SSetS SSetR </S>
         </sigma>
         <id> _ </id>
       </goroutine>
       <goroutine> // Partner receiver
         <k> <- channel(Ref:Int) => V </k>
         <sigma>
           <HB> HMapR:Map => mergeHB( HMapS, HMapR ) </HB>
           <S>  SSetR:Set => SSetS SSetR </S>
         </sigma>
         <select>_</select>
         <id> _ </id>
       </goroutine>
       <Chan>
         <ref> Ref </ref>
         <type> _ </type>
         <forward> .List </forward>
         <backward> .List </backward>
       </Chan>
  rule <goroutine> // Sender
         <id> _ </id>
         <k> selAux(.K) => selClear ~> Ts[$unit/Zs] ... </k>
         <select>
           ...
           <selBranch> (let Zs:Id = channel(Ref:Int) <- V:Val in Ts:Term):LetChan </selBranch>
           ...
         </select>
         <sigma>
           <HB> HMapS:Map => mergeHB( HMapS, HMapR ) </HB>
           <S>  SSetS:Set => SSetS SSetR </S>
         </sigma>
       </goroutine>
       <goroutine> // Receiver
         <id> _ </id>
         <k> selAux(.K) => selClear ~> Tr[V/Zr] ... </k>
         <selBranch> (let Zr:Id = <- channel(Ref:Int) in Tr:Term):LetChan </selBranch>
         <sigma>
           <HB> HMapR:Map => mergeHB( HMapS, HMapR ) </HB>
           <S>  SSetR:Set => SSetS SSetR </S>
         </sigma>
       </goroutine>
       <Chan>
         <ref> Ref:Int </ref>
         <type> _ </type>
         <forward> .List </forward>
         <backward> .List </backward>
       </Chan>

  // The default rule
  rule <goroutine>
         <k> selAux(.K) => selClear ~> T[default/Z] ... </k>
         <select>
           ...
           <selBranch> (let Z:Id = default in T:Term):LetDef </selBranch>
           ...
         </select>
         <sigma> _ </sigma>
         <id> _ </id>
       </goroutine> [owise]


endmodule
