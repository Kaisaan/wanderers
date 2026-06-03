from libwanderers.text import fix_ascii

def generate_asm(strings_filename, rows):
    """
    Generate strings.asm
    """
    with open(strings_filename, "w", encoding="utf-8") as asm_fp:
        for row in rows:
            
            if row[2] == "":
                continue
            en = row[2]
            en = fix_ascii(en)
            en = en.replace("\n", "\\n")
            
            if en.startswith("b\"\\x"):       # Add support to just put singular byte (python byte-string styled)
                en = "0x" + en.lstrip("b\"\\x").rstrip("\"")
            else: 
                en = "\"" + en.replace('"', '\\"') + "\""

            label = row[3]
            label = "L" + label

            asm_fp.write(f"{label}: equ\t{en}\n")