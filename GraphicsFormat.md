# GBXA2000 File Format
This is for files that have the `GBXA2000` identifier. For info on graphics files that use the `NAXA5010` format see the [documentation on Lost Kefin's repo](https://github.com/Kaisaan/lostkefin/blob/main/graphicsFormat.md)  
**Note: All values are stored in Little Endian unless otherwise specified.**

## Header

|Offset|Description|
|---|---|
|$00-$07|Always `47 42 58 41 32 30 30 30` or `GBXA2000` in ASCII|
|$08-$0B|Palette size , either $10 or $100|
|$0C-$0F|Palette Data offset, always `$20000000`|
|$10-$13|Offset to Image Data|
|$14-$15|Height of Tiles|
|$16-$17|Width of Tiles|
|$18-$19|Height of Graphic in Tiles|
|$1A-$1B|Width of Graphic in Tiles|
|$1C-$1D|Height of Graphic in Pixels|
|$1E-$1F|Width of Graphic in Pixels|

## Palette

The Palette (or CLUT) data always starts at $20 in the file and is either $10 colours or $100 colours. Each colour is 32 bits in RGBA8 format  
The size of the palette determines if the image data is either 4 bits per pixel or 8 bits per pixel respectively  
**The Palette data is Swizzled**

## Tiles

Each image is made up of tiles based on the header info. They are stored row-by-row starting from the top-left-most tile.  
Each tile's data is indexed based on the palette info.