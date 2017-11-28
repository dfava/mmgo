// Copyright (C) 2017 Daniel Fava. All Rights Reserved.
require "mmgo-syntax.k"
require "mmgo-common.k"

module MMGO-GO
  imports MMGO-SYNTAX
  imports MMGO-COMMON

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
