.ps2

// Redirect the original ending-sequence callsite to the codecave copy.
.org 0x17a5b8
jal play_ending_sequence
