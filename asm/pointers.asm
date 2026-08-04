.loadtable "asm/wanderers.tbl", "UTF8"

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

@L15AC90: .str L15AC90
@L15ACA8: .str L15ACA8
@L15ACB0: .str L15ACB0
@L15ACC8: .str L15ACC8
@L15ACD8: .str L15ACD8
@L15ACE8: .str L15ACE8
@L15ACF8: .str L15ACF8
@L15AD08: .str L15AD08
@L15AD18: .str L15AD18
@L15AD30: .str L15AD30
@L15AD48: .str L15AD48
@L15AD58: .str L15AD58
@L15AD68: .str L15AD68
@L15AD78: .str L15AD78
@L15AD88: .str L15AD88
@L15ADA0: .str L15ADA0
@L15ADB8: .str L15ADB8
@L15ADC8: .str L15ADC8
@L15ADD8: .str L15ADD8
@L15ADE8: .str L15ADE8
@L15ADF0: .str L15ADF0
@L15AE00: .str L15AE00
@L15AE10: .str L15AE10
@L15AE20: .str L15AE20

// Character Names

.orga 0x14DFA8

@L14DFA8: .str L14DFA8
@L14DFB0: .str L14DFB0
@L14DFB8: .str L14DFB8
@L14DFC8: .str L14DFC8
@L14DFD0: .str L14DFD0
@L14DFE0: .str L14DFE0
@L14DFE8: .str L14DFE8
@L14DFF0: .str L14DFF0
@L14E000: .str L14E000
@L14E010: .str L14E010
@L14E018: .str L14E018
@L14E028: .str L14E028
@L14E038: .str L14E038
@L14E048: .str L14E048
@L14E058: .str L14E058
@L14E060: .str L14E060
@L14E068: .str L14E068
@L14E078: .str L14E078
@L14E080: .str L14E080
@L14E088: .str L14E088

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

// Save Filename?

.orga 0x14E2B0 :: @L14E2B0 : .str L14E2B0
.orga 0x15F1D8 :: .dw @L14E2B0

// Area Name pointers

.orga 0x134890

.dw @L14E340
.dw @L14E350
.dw @L14E370
.dw @L14E370
.dw @L14E350
.dw @L14E388
.dw @L14E398
.dw @L14E398
.dw @L14E3A8
.dw @L14E3B8
.dw @L14E3C8
.dw @L14E3D8
.dw @L14E3E8
.dw @L14E3F8
.dw @L14E408
.dw @L14E418
.dw @L14E428
.dw @L14E438
.dw @L14E448
.dw @L14E458
.dw @L14E468
.skip 4         // Difficulty options
.dw @L14E478
.dw @L14E480
.dw @L14E488

// Area Name Text

.orga 0x14E340

@L14E340: .str L14E340
@L14E350: .str L14E350
@L14E370: .str L14E370
@L14E388: .str L14E388
@L14E398: .str L14E398
@L14E3A8: .str L14E3A8
@L14E3B8: .str L14E3B8
@L14E3C8: .str L14E3C8
@L14E3D8: .str L14E3D8
@L14E3E8: .str L14E3E8
@L14E3F8: .str L14E3F8
@L14E408: .str L14E408
@L14E418: .str L14E418
@L14E428: .str L14E428
@L14E438: .str L14E438
@L14E448: .str L14E448
@L14E458: .str L14E458
@L14E468: .str L14E468

// Difficulty options

@L14E478: .str L14E478
@L14E480: .str L14E480
@L14E488: .str L14E488

// Tutorial Text Pointers

.orga 0x134C90

.dw @L14F1A0
.dw @L14F1E0
.dw @L14F250
.dw @L14F2C0
.dw @L14F320



// Pause Menu Text Pointers

.orga 0x134D30

.dw @L14F550
.dw @L14F558
.dw @L14F560
.dw @L14F550
.dw @L14F568
.dw @L14F560

// Pause Menu Text

.orga 0x14F550

@L14F550: .str L14F550
@L14F558: .str L14F558
@L14F560: .str L14F560
@L14F568: .str L14F568

// Menu Pointers

.orga 0x1351B0

.dw @L14F5C0
.dw @L14F5E0
.dw @L14F600
.dw @L14F620
.dw @L14F640
.dw @L14F660
.dw @L14F680
.dw @L14F6A0
.dw @L14F6B8
.dw @L14F6C0
.dw @L14F6D0
.skip 4
.dw @L14F6D8
.dw @L14F6E0
.dw @L14F6E8

// Menu Text

.orga 0x14F5C0

@L14F5C0: .str L14F5C0
@L14F5E0: .str L14F5E0
@L14F600: .str L14F600
@L14F620: .str L14F620
@L14F640: .str L14F640
@L14F660: .str L14F660
@L14F680: .str L14F680
@L14F6A0: .str L14F6A0
@L14F6B8: .str L14F6B8
@L14F6C0: .str L14F6C0
@L14F6D0: .str L14F6D0
@L14F6D8: .str L14F6D8
@L14F6E0: .str L14F6E0
@L14F6E8: .str L14F6E8

// Item Pointers

.orga 0x135240

.dw @L14F740
.dw @L14F760
.dw @L14F7C0
.dw @L14F820
.dw @L14F880
.dw @L14F8E0
.dw @L14F950
.dw @L14F970
.dw @L14F9C0
.dw @L14FA30
.dw @L14FAA0
.dw @L14FB10
.dw @L14FB80
.dw @L14FBF0
.dw @L14FC60
.dw @L14FCD0
.dw @L14FD40
.dw @L14FDB0
.dw @L14FE00
.dw @L14FE70
.dw @L14FEE0
.dw @L14FF50
.dw @L14FFB0
.dw @L150020
.dw @L150080
.dw @L1500F0
.dw @L150160
.dw @L1501D0
.dw @L150240
.dw @L1502B0
.dw @L150310
.dw @L150380
.dw @L1503F0
.dw @L150450
.dw @L1504B0
.dw @L150520
.dw @L150590
.dw @L1505D0
.dw @L150620
.dw @L150660
.dw @L1506B0
.dw @L1506F0
.dw @L150740
.dw @L1507A0
.dw @L1507F0
.dw @L150840
.dw @L1508A0
.dw @L1508E0
.dw @L150930
.dw @L150980
.dw @L1509F0
.dw @L150A20
.dw @L150A80
.dw @L150A90
.dw @L150AA0
.dw @L150AB0
.dw @L150AC0
.dw @L150AD8
.dw @L150AE8
.dw @L150AF8
.dw @L150B10
.dw @L150B28
.dw @L150B38
.dw @L150B50
.dw @L150B68
.dw @L150B78
.dw @L150B88
.dw @L150B98
.dw @L150BA8
.dw @L150BB8
.dw @L150BC8
.dw @L150BD8
.dw @L150BE8
.dw @L150BF0
.dw @L150C00
.dw @L150C10
.dw @L150C20
.dw @L150C30
.dw @L150C40
.dw @L150C50
.dw @L150C60
.dw @L150C70
.dw @L150C80
.dw @L150C98
.dw @L150CA8
.dw @L150CB8
.dw @L150CC8
.dw @L150CD8
.dw @L150CE8
.dw @L150CF8
.dw @L150D08
.dw @L150D18
.dw @L150D28
.skip 12
.dw @L150D38
.dw @L150D38
.dw @L150D48
.dw @L150D58
.dw @L150D68

// Shop Name Pointers

.orga 0x1353E4 :: .dw @L150D78
.orga 0x13543C :: .dw @L150D80

// Item Text

.orga 0x14F740

@L14F740: .str L14F740
@L14F760: .str L14F760
@L14F7C0: .str L14F7C0
@L14F820: .str L14F820
@L14F880: .str L14F880
@L14F8E0: .str L14F8E0
@L14F950: .str L14F950
@L14F970: .str L14F970
@L14F9C0: .str L14F9C0
@L14FA30: .str L14FA30
@L14FAA0: .str L14FAA0
@L14FB10: .str L14FB10
@L14FB80: .str L14FB80
@L14FBF0: .str L14FBF0
@L14FC60: .str L14FC60
@L14FCD0: .str L14FCD0
@L14FD40: .str L14FD40
@L14FDB0: .str L14FDB0
@L14FE00: .str L14FE00
@L14FE70: .str L14FE70
@L14FEE0: .str L14FEE0
@L14FF50: .str L14FF50
@L14FFB0: .str L14FFB0
@L150020: .str L150020
@L150080: .str L150080
@L1500F0: .str L1500F0
@L150160: .str L150160
@L1501D0: .str L1501D0
@L150240: .str L150240
@L1502B0: .str L1502B0
@L150310: .str L150310
@L150380: .str L150380
@L1503F0: .str L1503F0
@L150450: .str L150450
@L1504B0: .str L1504B0
@L150520: .str L150520
@L150590: .str L150590
@L1505D0: .str L1505D0
@L150620: .str L150620
@L150660: .str L150660
@L1506B0: .str L1506B0
@L1506F0: .str L1506F0
@L150740: .str L150740
@L1507A0: .str L1507A0
@L1507F0: .str L1507F0
@L150840: .str L150840
@L1508A0: .str L1508A0
@L1508E0: .str L1508E0
@L150930: .str L150930
@L150980: .str L150980
@L1509F0: .str L1509F0
@L150A20: .str L150A20
@L150A80: .str L150A80
@L150A90: .str L150A90
@L150AA0: .str L150AA0
@L150AB0: .str L150AB0
@L150AC0: .str L150AC0
@L150AD8: .str L150AD8
@L150AE8: .str L150AE8
@L150AF8: .str L150AF8
@L150B10: .str L150B10
@L150B28: .str L150B28
@L150B38: .str L150B38
@L150B50: .str L150B50
@L150B68: .str L150B68
@L150B78: .str L150B78
@L150B88: .str L150B88
@L150B98: .str L150B98
@L150BA8: .str L150BA8
@L150BB8: .str L150BB8
@L150BC8: .str L150BC8
@L150BD8: .str L150BD8
@L150BE8: .str L150BE8
@L150BF0: .str L150BF0
@L150C00: .str L150C00
@L150C10: .str L150C10
@L150C20: .str L150C20
@L150C30: .str L150C30
@L150C40: .str L150C40
@L150C50: .str L150C50
@L150C60: .str L150C60
@L150C70: .str L150C70
@L150C80: .str L150C80
@L150C98: .str L150C98
@L150CA8: .str L150CA8
@L150CB8: .str L150CB8
@L150CC8: .str L150CC8
@L150CD8: .str L150CD8
@L150CE8: .str L150CE8
@L150CF8: .str L150CF8
@L150D08: .str L150D08
@L150D18: .str L150D18
@L150D28: .str L150D28
@L150D38: .str L150D38
@L150D48: .str L150D48
@L150D58: .str L150D58
@L150D68: .str L150D68

// Shop Name Text

@L150D78: .str L150D78
@L150D80: .str L150D80

// Shop Text Pointers

.orga 0x135490

.dw @L150D90
.dw @L150DB0
.dw @L150DD0
.dw @L150E20
.dw @L150E50
.dw @L150E70
.dw @L150E90
.dw @L150EE0
.dw @L150F00
.dw @L150E50
.dw @L150F18
.dw @L150F30
.dw @L150F60
.dw @L150FB0
.skip 8
.dw @L151000
.dw @L151020
.dw @L151040
.dw @L151060
.dw @L151080
.dw @L1510A0
.dw @L1510F0
.dw @L151140
.dw @L151190
.dw @L150F00
.dw @L1511A0
.dw @L1511C0

// Shop Text

.orga 0x150D90

@L150D90: .str L150D90
@L150DB0: .str L150DB0
@L150DD0: .str L150DD0
@L150E20: .str L150E20
@L150E50: .str L150E50
@L150E70: .str L150E70
@L150E90: .str L150E90
@L150EE0: .str L150EE0
@L150F00: .str L150F00
@L150F18: .str L150F18
@L150F30: .str L150F30
@L150F60: .str L150F60
@L150FB0: .str L150FB0
@L151000: .str L151000
@L151020: .str L151020
@L151040: .str L151040
@L151060: .str L151060
@L151080: .str L151080
@L1510A0: .str L1510A0
@L1510F0: .str L1510F0
@L151140: .str L151140
@L151190: .str L151190
@L1511A0: .str L1511A0
@L1511C0: .str L1511C0

// What Pointers

.orga 0x135524

.dw @L151228 :: .skip 20
.dw @L151230 :: .skip 20
.dw @L151240 :: .skip 20
.dw @L151248 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151258 :: .skip 20
.dw @L151260 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151270 :: .skip 20
.dw @L151278 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151288 :: .skip 20
.dw @L151298 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L1512A8 :: .skip 20
.dw @L1512B8 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L1512C8 :: .skip 20
.dw @L1512D8 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L1512E8 :: .skip 20
.dw @L1512F8 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151308 :: .skip 20
.dw @L151310 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151330 :: .skip 20
.dw @L151340 :: .skip 20
.dw @L151360 :: .skip 20
.dw @L151370 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151380 :: .skip 20
.dw @L151390 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L1513A0 :: .skip 20
.dw @L1513B0 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L1513C0 :: .skip 20
.dw @L1513C8 :: .skip 20
.dw @L1513D8 :: .skip 20
.dw @L1513E8 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L1513F8 :: .skip 20
.dw @L151408 :: .skip 20
.dw @L151418 :: .skip 20
.dw @L151428 :: .skip 20
.dw @L151438 :: .skip 20
.dw @L151448 :: .skip 20
.dw @L151458 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151460 :: .skip 20
.dw @L151470 :: .skip 20
.dw @L151478 :: .skip 20
.dw @L151488 :: .skip 20
.dw @L151498 :: .skip 20
.dw @L1514A8 :: .skip 20
.dw @L1514B8 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L1514C8 :: .skip 20
.dw @L1514D8 :: .skip 20
.dw @L1514E8 :: .skip 20
.dw @L1514F8 :: .skip 20
.dw @L151510 :: .skip 20
.dw @L151528 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151538 :: .skip 20
.dw @L151548 :: .skip 20
.dw @L151558 :: .skip 20
.dw @L151568 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151578 :: .skip 20
.dw @L151580 :: .skip 20
.dw @L151598 :: .skip 20
.dw @L1515A8 :: .skip 20
.dw @L1515B8 :: .skip 20
.dw @L1515C8 :: .skip 20
.dw @L1515D0 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L1515E8 :: .skip 20
.dw @L1515F8 :: .skip 20
.dw @L151608 :: .skip 20
.dw @L151618 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151628 :: .skip 20
.dw @L151630 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151640 :: .skip 20
.dw @L151658 :: .skip 20
.dw @L151670 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151690 :: .skip 20
.dw @L1516A0 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L1516B8 :: .skip 20
.dw @L1516C0 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20
.dw @L151228 :: .skip 20

// Ending Text Pointers

.orga 0x136130

// Ending Text 1 Pointers

.dw @L1516E0
.dw @L151700
.dw @L151720
.skip 4
.dw @L151740
.dw @L151770
.dw @L1517A0
.dw @L1517D0
.dw @L151800
.skip 4
.dw @L151820
.dw @L151840
.dw @L151860
.dw @L151880
.dw @Lcredits
.dw @L1518B0
.dw @L1518D0
.dw 0x00
.dw @L151900
.dw @L151920
.dw @L151940
.dw @L151960
.dw @L151990
.dw @L1519C0
.dw 0x00
.dw @L1519E0
.dw @L151A10
.dw @L151A40
.dw 0x00
.dw @L151A80
.dw @L151AA0
.dw 0x00
.dw @L151AD0
.dw @L151AF0
.skip 60
.dw @L151B10

// Ending text 2

.orga 0x136200

.dw @L1516E0
.dw @L151700
.dw @L151720
.skip 4
.dw @L151740
.dw @L151770
.dw @L1517A0
.dw @L1517D0
.dw @L151800
.skip 4
.dw @L151820
.dw @L151840
.dw @L151860
.dw @L151880
.dw @Lcredits
.dw 0x00
.dw @L151900
.dw @L151920
.dw @L151940
.dw @L151960
.dw @L151990
.dw @L1519C0
.dw 0x00
.dw @L1519E0
.dw @L151A10
.dw @L151A40
.dw 0x00
.dw @L151A80
.dw @L151AA0
.dw 0x00
.dw @L151AD0
.dw @L151AF0
.skip 60
.dw @L151B10

// Ending text 3 Pointers

.dw @L1516E0
.dw @L151700
.dw @L151720
.dw 0x00
.dw @L151740
.dw @L151770
.dw @L1517A0
.dw @L1517D0
.dw @L151800
.dw 0x00
.dw @L151B20
.dw @L151B50
.dw @L151B70
.dw 0x00
.dw @L151900
.dw @L151920
.dw @L151940
.dw @L151960
.dw @L151990
.dw @L1519C0
.dw 0x00
.dw @L1519E0
.dw @L151A10
.dw @L151A40
.dw 0x00
.dw @L151A80
.dw @L151AA0
.dw 0x00
.dw @L151AD0
.dw @L151AF0
.skip 60
.dw 0x00
.dw @L151B10

// Credits Text

.orga 0x151228

@L151228: credstr_151228: .str L151228
@L151230: credstr_151230: .str L151230
@L151240: credstr_151240: .str L151240
@L151248: credstr_151248: .str L151248
@L151258: credstr_151258: .str L151258
@L151260: credstr_151260: .str L151260
@L151270: credstr_151270: .str L151270
@L151278: credstr_151278: .str L151278
@L151288: credstr_151288: .str L151288
@L151298: credstr_151298: .str L151298
@L1512A8: credstr_1512A8: .str L1512A8
@L1512B8: credstr_1512B8: .str L1512B8
@L1512C8: credstr_1512C8: .str L1512C8
@L1512D8: credstr_1512D8: .str L1512D8
@L1512E8: credstr_1512E8: .str L1512E8
@L1512F8: credstr_1512F8: .str L1512F8
@L151308: credstr_151308: .str L151308
@L151310: credstr_151310: .str L151310
@L151330: credstr_151330: .str L151330
@L151340: credstr_151340: .str L151340
@L151360: credstr_151360: .str L151360
@L151370: credstr_151370: .str L151370
@L151380: credstr_151380: .str L151380
@L151390: credstr_151390: .str L151390
@L1513A0: credstr_1513A0: .str L1513A0
@L1513B0: credstr_1513B0: .str L1513B0
@L1513C0: credstr_1513C0: .str L1513C0
@L1513C8: credstr_1513C8: .str L1513C8
@L1513D8: credstr_1513D8: .str L1513D8
@L1513E8: credstr_1513E8: .str L1513E8
@L1513F8: credstr_1513F8: .str L1513F8
@L151408: credstr_151408: .str L151408
@L151418: credstr_151418: .str L151418
@L151428: credstr_151428: .str L151428
@L151438: credstr_151438: .str L151438
@L151448: credstr_151448: .str L151448
@L151458: credstr_151458: .str L151458
@L151460: credstr_151460: .str L151460
@L151470: credstr_151470: .str L151470
@L151478: credstr_151478: .str L151478
@L151488: credstr_151488: .str L151488
@L151498: credstr_151498: .str L151498
@L1514A8: credstr_1514A8: .str L1514A8
@L1514B8: credstr_1514B8: .str L1514B8
@L1514C8: credstr_1514C8: .str L1514C8
@L1514D8: credstr_1514D8: .str L1514D8
@L1514E8: credstr_1514E8: .str L1514E8
@L1514F8: credstr_1514F8: .str L1514F8
@L151510: credstr_151510: .str L151510
@L151528: credstr_151528: .str L151528
@L151538: credstr_151538: .str L151538
@L151548: credstr_151548: .str L151548
@L151558: credstr_151558: .str L151558
@L151568: credstr_151568: .str L151568
@L151578: credstr_151578: .str L151578
@L151580: credstr_151580: .str L151580
@L151598: credstr_151598: .str L151598
@L1515A8: credstr_1515A8: .str L1515A8
@L1515B8: credstr_1515B8: .str L1515B8
@L1515C8: credstr_1515C8: .str L1515C8
@L1515D0: credstr_1515D0: .str L1515D0
@L1515E8: credstr_1515E8: .str L1515E8
@L1515F8: credstr_1515F8: .str L1515F8
@L151608: credstr_151608: .str L151608
@L151618: credstr_151618: .str L151618
@L151628: credstr_151628: .str L151628
@L151630: credstr_151630: .str L151630
@L151640: credstr_151640: .str L151640
@L151658: credstr_151658: .str L151658
@L151670: credstr_151670: .str L151670
@L151690: credstr_151690: .str L151690
@L1516A0: credstr_1516A0: .str L1516A0
@L1516B8: credstr_1516B8: .str L1516B8
@L1516C0: credstr_1516C0: .str L1516C0

// Ending Text

@L1516E0: .str L1516E0
@L151700: .str L151700
@L151720: .str L151720
@L151740: .str L151740
@L151770: .str L151770
@L1517A0: .str L1517A0
@L1517D0: .str L1517D0
@L151800: .str L151800
@L151820: .str L151820
@L151840: .str L151840
@L151860: .str L151860
@L151880: .str L151880
@Lcredits: .str Lcredits
@L1518B0: .str L1518B0
@L1518D0: .str L1518D0
@L151900: .str L151900
@L151920: .str L151920
@L151940: .str L151940
@L151960: .str L151960
@L151990: .str L151990
@L1519C0: .str L1519C0
@L1519E0: .str L1519E0
@L151A10: .str L151A10
@L151A40: .str L151A40
@L151A80: .str L151A80
@L151AA0: .str L151AA0
@L151AD0: .str L151AD0
@L151AF0: .str L151AF0
@L151B10: .str L151B10
@L151B20: .str L151B20
@L151B50: .str L151B50
@L151B70: .str L151B70

// Item Get Text Pointers

.orga 0xD6EE0

.dw @L148060
.dw @L148070
.dw @L148070
.dw @L148070
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148070
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148070
.dw @L148060
.dw @L148060
.dw @L148070
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148070
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148060
.dw @L148070
.dw @L148070
.dw @L148060
.dw @L148070
.dw @L148060

// Put text here (seems to be unused)

.orga 0x145A88

// Tutorial Text

@L14F1A0: .str L14F1A0
@L14F1E0: .str L14F1E0
@L14F250: .str L14F250
@L14F2C0: .str L14F2C0
@L14F320: .str L14F320

// Item Get text

@L148060: .str L148060
@L148070: .str L148070

// Hardcoded stuff (Has no pointers)

.orga 0x14E490 :: @L14E490: .str L14E490 // Yes   No Text
// .orga 0x14E4A0 :: @L14E4A0: .str L14E4A0 // は Ha (unknown)
.orga 0x14E4A8 :: @L14E4A8: .str L14E4A8 // A (unknown)
.orga 0x14E4B0 :: @L14E4B0: .str L14E4B0 // No Data

.orga 0x14E4C0 :: @L14E4C0: .str L14E4C0
.orga 0x14E4F0 :: @L14E4F0: .str L14E4F0
.orga 0x14E520 :: @L14E520: .str L14E520
.orga 0x14E560 :: @L14E560: .str L14E560
.orga 0x14E5C0 :: @L14E5C0: .str L14E5C0
.orga 0x14E5F0 :: @L14E5F0: .str L14E5F0
.orga 0x14E6A0 :: @L14E6A0: .str L14E6A0
.orga 0x14E6C0 :: @L14E6C0: .str L14E6C0
.orga 0x14E6F0 :: @L14E6F0: .str L14E6F0
.orga 0x14E780 :: @L14E780: .str L14E780
.orga 0x14E7A0 :: @L14E7A0: .str L14E7A0
.orga 0x14E7D0 :: @L14E7D0: .str L14E7D0
.orga 0x14E7F0 :: @L14E7F0: .str L14E7F0
.orga 0x14E880 :: @L14E880: .str L14E880
.orga 0x14E900 :: @L14E900: .str L14E900
.orga 0x14E9A0 :: @L14E9A0: .str L14E9A0
.orga 0x14E9D0 :: @L14E9D0: .str L14E9D0
.orga 0x14EA70 :: @L14EA70: .str L14EA70
.orga 0x14EAC0 :: @L14EAC0: .str L14EAC0
.orga 0x14EBF0 :: @L14EBF0: .str L14EBF0
.orga 0x14ECA0 :: @L14ECA0: .str L14ECA0
.orga 0x14EDA0 :: @L14EDA0: .str L14EDA0
.orga 0x14EDD0 :: @L14EDD0: .str L14EDD0
.orga 0x14EE00 :: @L14EE00: .str L14EE00
.orga 0x14EE30 :: @L14EE30: .str L14EE30
.orga 0x14EE50 :: @L14EE50: .str L14EE50
.orga 0x14EE78 :: @L14EE78: .str L14EE78
.orga 0x14EE80 :: @L14EE80: .str L14EE80
.orga 0x14EE88 :: @L14EE88: .str L14EE88
.orga 0x14EEA0 :: @L14EEA0: .str L14EEA0

.orga 0x14F570 :: @L14F570: .str L14F570
.orga 0x14F578 :: @L14F578: .str L14F578
.orga 0x14F5A8 :: @L14F5A8: .str L14F5A8
.orga 0x14F5B0 :: @L14F5B0: .str L14F5B0

.orga 0x1511D8 :: @L1511D8: .str L1511D8
.orga 0x1511E8 :: @L1511E8: .str L1511E8
.orga 0x151200 :: @L151200: .str L151200
.orga 0x151218 :: @L151218: .str L151218

.orga 0x15AE48 :: @L15AE48: .str L15AE48
.orga 0x15AE50 :: @L15AE50: .str L15AE50
.orga 0x15AE58 :: @L15AE58: .str L15AE58
.orga 0x15AE60 :: @L15AE60: .str L15AE60
.orga 0x15AE68 :: @L15AE68: .str L15AE68
.orga 0x15AE70 :: @L15AE70: .str L15AE70
.orga 0x15AE78 :: @L15AE78: .str L15AE78
.orga 0x15AE80 :: @L15AE80: .str L15AE80
.orga 0x15AE88 :: @L15AE88: .str L15AE88
.orga 0x15AE90 :: @L15AE90: .str L15AE90
.orga 0x15AE98 :: @L15AE98: .str L15AE98
.orga 0x15AEA0 :: @L15AEA0: .str L15AEA0
.orga 0x15AEA8 :: @L15AEA8: .str L15AEA8
.orga 0x15EB20 :: @L15EB20: .str L15EB20
.orga 0x15EB28 :: @L15EB28: .str L15EB28
.orga 0x15EB30 :: @L15EB30: .str L15EB30
.orga 0x15EB38 :: @L15EB38: .str L15EB38
.orga 0x15EB40 :: @L15EB40: .str L15EB40
.orga 0x15EB48 :: @L15EB48: .str L15EB48
.orga 0x15EB50 :: @L15EB50: .str L15EB50
.orga 0x15EB58 :: @L15EB58: .str L15EB58
.orga 0x15EB60 :: @L15EB60: .str L15EB60
.orga 0x15EB68 :: @L15EB68: .str L15EB68
.orga 0x15EB78 :: @L15EB78: .str L15EB78
.orga 0x15EB80 :: @L15EB80: .str L15EB80
.orga 0x15EB88 :: @L15EB88: .str L15EB88
.orga 0x15EB90 :: @L15EB90: .str L15EB90
.orga 0x15EB98 :: @L15EB98: .str L15EB98
.orga 0x15EBA0 :: @L15EBA0: .str L15EBA0
.orga 0x15EBA8 :: @L15EBA8: .str L15EBA8
.orga 0x15EBB0 :: @L15EBB0: .str L15EBB0
.orga 0x15EBB8 :: @L15EBB8: .str L15EBB8
.orga 0x15EBC0 :: @L15EBC0: .str L15EBC0
.orga 0x15EBC8 :: @L15EBC8: .str L15EBC8
.orga 0x15EBD0 :: @L15EBD0: .str L15EBD0
.orga 0x15EBD8 :: @L15EBD8: .str L15EBD8
.orga 0x15EBE0 :: @L15EBE0: .str L15EBE0
.orga 0x15EBE8 :: @L15EBE8: .str L15EBE8
.orga 0x15EBF0 :: @L15EBF0: .str L15EBF0
.orga 0x15EBF8 :: @L15EBF8: .str L15EBF8
.orga 0x15EC00 :: @L15EC00: .str L15EC00
.orga 0x15EC08 :: @L15EC08: .str L15EC08
.orga 0x15EC10 :: @L15EC10: .str L15EC10
.orga 0x15EC20 :: @L15EC20: .str L15EC20
.orga 0x15EC40 :: @L15EC40: .str L15EC40
.orga 0x15EC60 :: @L15EC60: .str L15EC60
.orga 0x15EC90 :: @L15EC90: .str L15EC90
.orga 0x15ECB0 :: @L15ECB0: .str L15ECB0
.orga 0x15ECD0 :: @L15ECD0: .str L15ECD0
.orga 0x15ECE0 :: @L15ECE0: .str L15ECE0
.orga 0x15ED00 :: @L15ED00: .str L15ED00
.orga 0x15EEA0 :: @L15EEA0: .str L15EEA0
.orga 0x15EEC0 :: @L15EEC0: .str L15EEC0
