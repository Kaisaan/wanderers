// Equip and event item description layout patches.

// move the backing panel left to match the text/icon.
.org 0x235040
.dw 0x12

// widen the backing panel for the translated text.
.org 0x235048
.dw 0x25c


////
// Equip menu.
////

// Move icon left
.org 0x001804c0
addiu a2,zero,0x14

// Move text left
.org 0x0017e0b8
addiu a1,zero,0x5c

.org 0x0017f0b8
addiu v0,zero,0x5c

// Move text down
.org 0x0017e0c0
addiu a2,zero,0x126

.org 0x0017f0c0
addiu a2,zero,0x126

.org 0x0017f1d0
addiu a2,zero,0x126

// Transition state patches
.org 0x0017f1c8
addiu a1,zero,-0x224

.org 0x0017f8a0
addiu v0,zero,0x5c

.org 0x0017f8a8
addiu a2,zero,0x126

.org 0x0017f9ac
addiu a1,zero,0x5c

.org 0x0017f9b4
addiu a2,zero,0x126


////
// Event item menu.
////

// Move icon left
.org 0x001806cc
addiu a2,zero,0x14

// Move text left
.org 0x0017f1d8
addiu a1,zero,0x5c


// Move text down

.org 0x0017f1e0
addiu a2,zero,0x126

.org 0x0017e848
addiu a2,zero,0x126

.org 0x0017f0dc
addiu a2,zero,0x126

.org 0x0017f9c4
addiu a2,zero,0x126

.org 0x0017f8c4
addiu a2,zero,0x126
