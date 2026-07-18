// Relocated copy of play_ending_sequence from SLPM_625.32.

play_ending_sequence:
addiu sp,sp,-0x30
addiu a0,zero,0x4
sd ra,0x10(sp)
addiu a1,zero,0x10
jal 0x0010f500
sq s0,0x0(sp)
lui a1,0x26
addiu a0,gp,-0x7b8c
addiu a1,a1,-0x11a8
jal 0x001821d0
addiu a2,zero,0x96
jal 0x00107660
sw v0,-0x7e50(gp)
sw v0,0x2c(sp)
lui a1,0x24
lw a0,0x2c(sp)
jal 0x00170ff0
addiu a1,a1,0x3c10
daddu s0,v0,zero
addiu a1,zero,0x56
daddu a0,s0,zero
jal 0x00107e50
addiu a2,zero,0x1
daddu a0,s0,zero
addiu a1,zero,0x61
jal 0x00107e50
addiu a2,zero,0x1
daddu a0,s0,zero
addiu a1,zero,0x5f
jal 0x00107e50
daddu a2,zero,zero
lw v0,-0x7c54(gp)
beq v0,zero,play_ending_sequence_audio_ready
daddu a0,zero,zero
jal 0x0015eb70
addiu a1,zero,0x80
play_ending_sequence_audio_ready:
lui v0,0x100
jal 0x00182a20
ori a0,v0,0x18
jal 0x0014c030
addiu a0,zero,0x10
jal 0x0012e5d0
nop
jal 0x00113cb0
daddu a0,v0,zero
daddu a0,v0,zero
jal 0x00113b60
addiu a1,zero,0x10
lui a0,0x23
addiu v0,zero,0x1
lui at,0x82
addiu a0,a0,0x5490
jal 0x001b0410
sw v0,-0x4020(at)
jal 0x001b0be0
nop
jal 0x0014c030
addiu a0,zero,0x10
jal 0x0012e5d0
nop
jal 0x00113cb0
daddu a0,v0,zero
daddu a0,v0,zero
jal 0x00113b60
addiu a1,zero,0x10
jal 0x001b1460
nop
// Preserve the Fin widget handle for the Triangle credits overlay.
sw v0,0x28(sp)
lw a0,0x2c(sp)
jal 0x00108600
daddu a1,v0,zero
// Add the Fan TL Credits prompt above the original Save and Title prompts.
li a0,ending_fan_tl_credits_prompt
addiu a1,zero,0x1b0
addiu a2,zero,0x118
jal 0x00110c40
daddu a3,zero,zero
// Preserve the Fan TL Credits prompt handle for the Triangle credits overlay.
sw v0,0x1c(sp)
daddu s0,v0,zero
addiu a1,zero,0x7
daddu a0,s0,zero
jal 0x00107e50
addiu a2,zero,0x258
daddu a0,s0,zero
addiu a1,zero,0x8
jal 0x00107e50
daddu a2,zero,zero
daddu a0,s0,zero
addiu a1,zero,0x56
jal 0x00107e50
addiu a2,zero,0x1
daddu a0,s0,zero
addiu a1,zero,0x61
jal 0x00107e50
addiu a2,zero,0x1
lw a0,0x2c(sp)
jal 0x00108600
daddu a1,s0,zero
lw a0,-0x7e58(gp)
addiu a1,zero,0x1b0
addiu a2,zero,0x138
jal 0x00110c40
daddu a3,zero,zero
// Preserve the Save prompt widget handle for the Triangle credits overlay.
sw v0,0x24(sp)
daddu s0,v0,zero
addiu a1,zero,0x7
daddu a0,s0,zero
jal 0x00107e50
addiu a2,zero,0x258
daddu a0,s0,zero
addiu a1,zero,0x8
jal 0x00107e50
daddu a2,zero,zero
daddu a0,s0,zero
addiu a1,zero,0x56
jal 0x00107e50
addiu a2,zero,0x1
daddu a0,s0,zero
addiu a1,zero,0x61
jal 0x00107e50
addiu a2,zero,0x1
lw a0,0x2c(sp)
jal 0x00108600
daddu a1,s0,zero
lw a0,-0x7e54(gp)
addiu a1,zero,0x1b0
addiu a2,zero,0x158
jal 0x00110c40
daddu a3,zero,zero
// Preserve the Title prompt widget handle for the Triangle credits overlay.
sw v0,0x20(sp)
daddu s0,v0,zero
addiu a1,zero,0x7
daddu a0,s0,zero
jal 0x00107e50
addiu a2,zero,0x258
daddu a0,s0,zero
addiu a1,zero,0x8
jal 0x00107e50
daddu a2,zero,zero
daddu a0,s0,zero
addiu a1,zero,0x56
jal 0x00107e50
addiu a2,zero,0x1
daddu a0,s0,zero
addiu a1,zero,0x61
jal 0x00107e50
addiu a2,zero,0x1
lw a0,0x2c(sp)
jal 0x00108600
daddu a1,s0,zero
play_ending_sequence_input_loop:
jal 0x0012e5d0
nop
jal 0x00113cb0
daddu a0,v0,zero
daddu a0,v0,zero
jal 0x00113b60
addiu a1,zero,0x1
lui at,0x7f
lhu v1,-0x5722(at)
andi v0,v1,0xa0
sltu v0,zero,v0
xori v0,v0,0x1
bne v0,zero,play_ending_sequence_check_cancel
lui v0,0x100
addiu s0,zero,0x1
jal 0x00182910
ori a0,v0,0x1b
b play_ending_sequence_cleanup
nop
nop
play_ending_sequence_check_cancel:
andi v0,v1,0x40
beq v0,zero,play_ending_sequence_check_custom_credits
lui v0,0x100
daddu s0,zero,zero
jal 0x00182910
ori a0,v0,0x1c
b play_ending_sequence_cleanup
nop
// Handle Triangle separately from the original Save and Title inputs.
play_ending_sequence_check_custom_credits:
andi v0,v1,0x10
beq v0,zero,play_ending_sequence_input_loop
nop
// Hide the Fin widget and all three prompts before running the custom credits.
lw a0,0x28(sp)
addiu a1,zero,0x56
jal 0x00107e50
daddu a2,zero,zero
lw a0,0x24(sp)
addiu a1,zero,0x56
jal 0x00107e50
daddu a2,zero,zero
lw a0,0x20(sp)
addiu a1,zero,0x56
jal 0x00107e50
daddu a2,zero,zero
lw a0,0x1c(sp)
addiu a1,zero,0x56
jal 0x00107e50
daddu a2,zero,zero
// Replace the ending music with BGM04 for the custom credits.
lui v0,0x100
jal 0x00182a20
ori a0,v0,0x4
// Run the relocated fan translation credits script with the custom tables.
li a0,credits_script
jal 0x001b0410
nop
// Fade BGM04 to silence over 120 frames before stopping it.
addiu s0,zero,0x78
play_ending_sequence_fade_custom_bgm:
addiu s0,s0,-0x1
lw v1,-0x7bd8(gp)
mult a0,s0,v1
addiu v0,zero,0x3c
div a0,v0
mflo a0
jal 0x001827c0
nop
jal 0x0012e5d0
nop
jal 0x00113cb0
daddu a0,v0,zero
daddu a0,v0,zero
jal 0x00113b60
addiu a1,zero,0x1
bgtz s0,play_ending_sequence_fade_custom_bgm
nop
jal 0x00182a80
nop
// Restore the Fin widget and all three prompts after the custom credits return.
lw a0,0x28(sp)
addiu a1,zero,0x56
jal 0x00107e50
addiu a2,zero,0x1
lw a0,0x24(sp)
addiu a1,zero,0x56
jal 0x00107e50
addiu a2,zero,0x1
lw a0,0x20(sp)
addiu a1,zero,0x56
jal 0x00107e50
addiu a2,zero,0x1
lw a0,0x1c(sp)
addiu a1,zero,0x56
jal 0x00107e50
addiu a2,zero,0x1
// Return to the ending prompt input loop after restoring the overlay.
b play_ending_sequence_input_loop
nop
play_ending_sequence_cleanup:
jal 0x0014c0a0
addiu a0,zero,0x10
jal 0x0012e5d0
nop
jal 0x00113cb0
daddu a0,v0,zero
daddu a0,v0,zero
jal 0x00113b60
addiu a1,zero,0x10
jal 0x00108450
addiu a0,sp,0x2c
jal 0x0013fc88
lw a0,-0x7b8c(gp)
jal 0x00182a80
nop
beq s0,zero,play_ending_sequence_return
addiu a0,zero,0x3
jal 0x0016fbd0
nop
nop
play_ending_sequence_return:
ld ra,0x10(sp)
lq s0,0x0(sp)
jr ra
addiu sp,sp,0x30

play_ending_sequence_end:
