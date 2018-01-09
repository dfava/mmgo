// Copyright (C) 2017 Daniel Fava. All Rights Reserved.
require "substitution.k"
require "mmgo-syntax.k"
require "mmgo-chans.k"

module MMGO-SELECT
  imports SUBSTITUTION
  imports MMGO-SYNTAX
  imports MMGO-CHANS

  /*
     For a synchronous branch to be enabled, a partner (another thread) must exist.
     It is not hard to envision the rule for GetSelBranchStatus for a synchronous branch
     where a partner exists and the GetSelBranchStatus returns "true"
     It is harder to envision a rule for when a partner does not exist.  The rule that
     evaluates to "false" (no partner exists) is a rule that fire when the rule that evaluates
     to "true" cannot fire.
     I suspect we can implement this with priorities:
     Give the rule that evals to "true" a priority higher than another rule that evals to "false".
  */

  syntax Val ::= "default"

  /*
     For every branch in the select statement
     Get the branch status (GetSelBranchStatus), which can be $En, $Closed, $Full, or $Def
     Go over all the branches creating a list of statuses then
     -> If $En and $Def not in the List, reconstruct the select statement
     -> If $En not in List and $Def in List, take the default
     -> If $En in List, make a random choice between all $En from the List
  */

  syntax SelBranchStatus ::= "$En" | "$Closed" | "$Full" | "$Empty" | "$Def"
  syntax KResult ::= SelBranchStatus
  syntax K ::= "GetSelBranchStatus" "(" LetChan ")"  [anywhere, structural]
  syntax K ::= "GetSelBranchStatus" "(" LetDef ")"   [anywhere, structural]
  //@ (send) Can never send on a closed channel
  rule <k> GetSelBranchStatus(let Z:Id = channel(Ref:Int) <- V:Val in T:Term) => $Closed ... </k>
       <chan>
         <ref> Ref </ref>
         <type> _ </type>
        <forward> FQ </forward>
        <backward> BQ </backward>
      </chan>
      requires EotInFQ( FQ ) ==Bool true // channel is closed
  /*@ (async send) Cannot send when channel is full (i.e. BQ is empty)
                   Can send when channel is not full (i.e. BQ is not empty) */
  rule <k> GetSelBranchStatus( let Z:Id = channel(Ref:Int) <- V:Val in T:Term ) => $En ... </k>
       <chan>
         <ref> Ref </ref>
         <type> _ </type>
        <forward> FQ </forward>
        <backward> BQ </backward>
      </chan>
      requires (EotInFQ(FQ) ==Bool false) // channel is open  
               andBool (size(FQ) +Int size(BQ) >Int 0) // channel is async
               andBool (size(BQ) >=Int 1) // channel not full
  rule <k> GetSelBranchStatus( let Z:Id = channel(Ref:Int) <- V:Val in T:Term ) => $Full ... </k>
       <chan>
         <ref> Ref </ref>
         <type> _ </type>
        <forward> FQ </forward>
        <backward> .List </backward> // channel is full
      </chan>
      requires (EotInFQ(FQ) ==Bool false) // channel is open  
               andBool (size(FQ) >Int 0) // channel is async
  syntax SelBranchStatus ::= "$Sync"
  /*@ (sync send) TODO */
  rule <k> GetSelBranchStatus( let Z:Id = channel(Ref:Int) <- V:Val in T:Term ) => $Sync ... </k>
       <chan>
         <ref> Ref </ref>
         <type> _ </type>
        <forward> .List </forward>
        <backward> .List </backward> // channel is synchronous and open
      </chan>

  //@ (receive) Can always receive on a closed channel
  rule <k> GetSelBranchStatus( let Z:Id = <- channel(Ref:Int) in T:Term ) => $En ... </k>
       <chan>
         <ref> Ref </ref>
         <type> _ </type>
        <forward> FQ </forward>
        <backward> BQ </backward>
      </chan>
      requires EotInFQ( FQ ) ==Bool true // channel is closed
  /*@ (async receive) Can receive when FQ is non-empty (i.e. channel is not empty),
                      including when queue is closed and EOT is in the FQ.
                      Cannot receive when FQ is empty (i.e. channel is empty) */
  rule <k> GetSelBranchStatus( let Z:Id = <- channel(Ref:Int) in T:Term ) => $En ... </k>
       <chan>
         <ref> Ref </ref>
         <type> _ </type>
        <forward> FQ </forward>
        <backward> BQ </backward>
      </chan>
      requires (EotInFQ(FQ) ==Bool false) // channel is open  
               andBool (size(FQ) +Int size(BQ) >Int 0) // channel is async
               andBool (size(FQ) >=Int 1)  // channel not empty
  rule <k> GetSelBranchStatus( let Z:Id = <- channel(Ref:Int) in T:Term ) => $Empty ... </k>
       <chan>
         <ref> Ref </ref>
         <type> _ </type>
        <forward> .List </forward>  // channel is empty and open
        <backward> BQ </backward>
      </chan>
      requires (size(BQ) >Int 0) // channel is async
  /*@ (sync receive) TODO */
  rule <k> GetSelBranchStatus( let Z:Id = <- channel(Ref:Int) in T:Term ) => $Sync ... </k>
       <chan>
         <ref> Ref </ref>
         <type> _ </type>
        <forward> .List </forward>
        <backward> .List </backward> // channel is synchronous and open
      </chan>

  rule GetSelBranchStatus( let Z:Id = default in T:Term ) => $Def



  syntax K ::=  "SelTraverseBs" "(" GBranch "," List ")" [anywhere, structural] // Auxiliary rule to gather the status of branches
  //@ Select
  rule <k> sel { Bs:GBranch } => SelTraverseBs(Bs, .List) ~> sel { Bs } ... </k>
  rule <k> SelTraverseBs({ BHead:LetChan }, L:List) =>  
            GetSelBranchStatus(BHead) ~> SelTraverseBs(., L) ... </k> // base case
  rule <k> SelTraverseBs({ BHead:LetDef  }, L:List) =>
            GetSelBranchStatus(BHead) ~> SelTraverseBs(., L) ... </k> // base case
  rule <k> SelTraverseBs({ BHead:LetChan } BTail:GBranch, L:List) =>
            GetSelBranchStatus(BHead) ~> SelTraverseBs(BTail, L) ... </k>

  rule <k> B:SelBranchStatus ~> SelTraverseBs(., L)      => SelTraverseBs(. , L ListItem(B)) ... </k>
  rule <k> B:SelBranchStatus ~> SelTraverseBs(Bs, L)     => SelTraverseBs(Bs, L ListItem(B) ) ... </k>

  syntax K ::= "SelPick" "(" Int "," K ")" // The second argument is for helping debug
  syntax K ::= "StatToIdx" "(" Set "," List "," Int "," K ")"  [anywhere, structural]
  // No branch is enabled and there is no default => Reconstruct the select statement
  rule SelTraverseBs( . , L:List) => SelPick(-1, L)
           requires notBool( ListItem($En) in L ) andBool notBool( ListItem($Def) in L )
  // There is default but no enabled branches => Take default (the last branch according to the syntax)
  rule SelTraverseBs( . , L:List) => SelPick(size(L) -Int 1, L)
           requires notBool( ListItem($En) in L ) andBool (ListItem($Def) in L)
  // There are enabled branches => Choose an enabled branch randomly
  rule SelTraverseBs( . , L:List) => StatToIdx(.Set, L, 0, L)
           requires ListItem($En) in L
  
  // From list of statuses to list of indexes whose statuses are En
  rule StatToIdx( Idxs, ListItem(S:SelBranchStatus) L, Cnt:Int, D ) =>
        StatToIdx( Idxs SetItem(Cnt), L, Cnt +Int 1, D )
        requires S ==K $En
  rule StatToIdx( Idxs, ListItem(S:SelBranchStatus) L, Cnt:Int, D ) =>
        StatToIdx( Idxs, L, Cnt +Int 1, D )
        requires S =/=K $En
  // Pick a random enabled branch
  rule StatToIdx( Idxs, .List, _, D ) => choice(Idxs) ~> SelPick(., D)
  rule Idx ~> SelPick(., D) => SelPick(Idx, D)

  rule SelPick(0, _ ) ~> sel{ { BHead } _     } => BHead
  rule SelPick(0, _ ) ~> sel{ { BHead:LetChan } } => BHead
  rule SelPick(0, _ ) ~> sel{ { BHead:LetDef  } } => BHead
  rule SelPick( (Idx => Idx -Int 1), _ ) ~> (sel{ {BHead} BTail } => sel{ BTail }) 
        requires (Idx >Int 0)

  rule (let Z:Id =       <- C:Val in T:Term):LetChan =>   <- C ~> let Z = $HOLE in T
  rule (let Z:Id = C:Val <- V:Val in T:Term):LetChan => C <- V ~> let Z = $HOLE in T
  rule (let Z:Id = default        in T:Term):LetDef  => T[default/Z]
  rule V:Val ~> let Z:Id = $HOLE in T:Term => let Z = V in T

endmodule
