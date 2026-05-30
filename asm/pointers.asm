.include "asm/strings.asm", "UTF8"

// Offset equ 0xFFF80

// Music pointers

.orga 0x00136E74

.dw @L15AC90 :: .skip 4
.dw @L15ACA8 :: .skip 4
.dw @L15ACB0 :: .skip 4
.dw @L15ACC8 :: .skip 4
.dw @L15ACD8 :: .skip 4
.dw @L15ACE8 :: .skip 4
.dw @L15ACF8 :: .skip 4
.dw @L15AD08 :: .skip 4
.dw @L15AD18 :: .skip 4
.dw @L15AD30 :: .skip 4
.dw @L15AD48 :: .skip 4
.dw @L15AD58 :: .skip 4
.dw @L15AD68 :: .skip 4
.dw @L15AD78 :: .skip 4
.dw @L15AD88 :: .skip 4
.dw @L15ADA0 :: .skip 4
.dw @L15ADB8 :: .skip 4
.dw @L15ADC8 :: .skip 4
.dw @L15ADD8 :: .skip 4
.dw @L15ADE8 :: .skip 4
.dw @L15ADF0 :: .skip 4
.dw @L15AE00 :: .skip 4
.dw @L15AE10 :: .skip 4
.dw @L15AE20 :: .skip 4

// Music Text

.orga 0x15AC90

@L15AC90: .asciiz L15AC90
@L15ACA8: .asciiz L15ACA8
@L15ACB0: .asciiz L15ACB0
@L15ACC8: .asciiz L15ACC8
@L15ACD8: .asciiz L15ACD8
@L15ACE8: .asciiz L15ACE8
@L15ACF8: .asciiz L15ACF8
@L15AD08: .asciiz L15AD08
@L15AD18: .asciiz L15AD18
@L15AD30: .asciiz L15AD30
@L15AD48: .asciiz L15AD48
@L15AD58: .asciiz L15AD58
@L15AD68: .asciiz L15AD68
@L15AD78: .asciiz L15AD78
@L15AD88: .asciiz L15AD88
@L15ADA0: .asciiz L15ADA0
@L15ADB8: .asciiz L15ADB8
@L15ADC8: .asciiz L15ADC8
@L15ADD8: .asciiz L15ADD8
@L15ADE8: .asciiz L15ADE8
@L15ADF0: .asciiz L15ADF0
@L15AE00: .asciiz L15AE00
@L15AE10: .asciiz L15AE10
@L15AE20: .asciiz L15AE20

// Character Names

.orga 0x14DFA8

@L14DFA8: .asciiz L14DFA8
@L14DFB0: .asciiz L14DFB0
@L14DFB8: .asciiz L14DFB8
@L14DFC8: .asciiz L14DFC8
@L14DFD0: .asciiz L14DFD0
@L14DFE0: .asciiz L14DFE0
@L14DFE8: .asciiz L14DFE8
@L14DFF0: .asciiz L14DFF0
@L14E000: .asciiz L14E000
@L14E010: .asciiz L14E010
@L14E018: .asciiz L14E018
@L14E028: .asciiz L14E028
@L14E038: .asciiz L14E038
@L14E048: .asciiz L14E048
@L14E058: .asciiz L14E058
@L14E060: .asciiz L14E060
@L14E068: .asciiz L14E068
@L14E078: .asciiz L14E078
@L14E080: .asciiz L14E080
@L14E088: .asciiz L14E088

// Character Name pointers

.orga 0x12D650

.dw @L14DFA8
.dw @L14DFB0
.dw @L14DFB8
.dw @L14DFC8
.dw @L14DFD0
.dw @L14DFE0
.dw @L14DFE8
.dw @L14DFE8
.dw @L14DFF0
.dw @L14DFE8
.dw @L14E000
.dw @L14DFE0
.dw @L14E010
.dw @L14E018
.dw @L14E028
.dw @L14E038
.dw @L14E048
.dw @L14E058
.dw @L14E060
.dw @L14E010
.dw @L14E010
.dw @L14E010
.dw @L14E010
.dw @L14E068
.dw @L14E078
.dw @L14E080
.dw @L14DFE8
.dw @L14DFE8
.dw @L14DFE8
.dw @L14DFE0
.dw @L14DFE0
.dw @L14E088

