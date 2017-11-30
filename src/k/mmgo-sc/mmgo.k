// Copyright (C) 2017 Daniel Fava. All Rights Reserved.
require "../mmgo/mmgo-syntax.k"
require "../mmgo/mmgo-local.k"
require "../mmgo/mmgo-chans.k"
require "../mmgo/mmgo-select.k"
require "../mmgo/mmgo-go.k"
require "mmgo-smem.k"

module MMGO
  imports MMGO-SYNTAX
  imports MMGO-LOCAL
  imports MMGO-CHANS
  imports MMGO-SELECT
  imports MMGO-GO
  imports MMGO-SMEM
  rule int .Globals; T => T      [structural]
endmodule
