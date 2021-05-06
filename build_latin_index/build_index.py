import sys
from typing import Any

from parse_combining import main as pc
from parse_raw import main as pr
from parse_raw_double import main as prd
from template import lookup_table

"""
Valid for LATIN charset (U+0000 - U+02AF)
Aggregate module for building latin.py that contains:
    STANDARD_STR: list[str]
    STANDARD_BYTES: list[bytes]
    NON_STANDARD_STR: list[str]
    NON_STANDARD_BYTES: list[bytes]
    STANDARD_MAP_BYTES: dict[bytes, bytes]
    STANDARD_MAP_STR: dict[str, str]
    SUPPORTED_RANGE: list[str]
    COMBINING_SUPPORTED: set[str]

The idea is to match special combining characters using 
    '''combining_full: set[str]'''
then substituing to native version of the grapheme using 
    '''standard_map_str: dict[str, str]'''
"""

combining: list[tuple[Any, ...]] = []
native: list[tuple[Any, ...]] = []
combining_ = pc()
native = pr()
native_double = prd()
# modifiers_str: list[str] = []
# modifiers: set[str] = set(modifiers_str)
# modifiers: set[str] = {i.decode("utf8") for i in modifiers_bytes}

lookup_table_combining: dict[str, str] = { k: v for (v, k) in combining_ }
combining_supported: set[str] = {
    lookup_table_combining[i] for i in 
    { m[2] for m in native }
}

# p: list[bytes] = [i.encode("utf8") for i in modifiers]
# pattern: re.Pattern = re.compile(b"|".join(p))
# modifiers_: set[str] = set(lookup_table_combining.values())

standard_str: list[str] = []
standard_bytes: list[bytes] = []
non_standard_str: list[str] = []
non_standard_bytes: list[bytes] = []

l: str
mod1: str
mod2: str
out_ns: str
for case, letter, modifier, out in native:
    l = lookup_table["LATIN"][case][letter]
    mod1 = lookup_table_combining[modifier]
    out_ns = l + mod1
    standard_str.append(out)
    standard_bytes.append(out.encode("utf8"))
    non_standard_str.append(out_ns)
    non_standard_bytes.append(out_ns.encode("utf8"))

# ATTENTION: ne tiens pas compte des combining doubles qui sont dans les extensions
for case, letter, modifier1, modifier2, out in native_double:
    l = lookup_table["LATIN"][case][letter]
    mod1 = lookup_table_combining[modifier1]
    mod2 = lookup_table_combining[modifier2]
    out_ns = l + mod1 + mod2
    standard_str.append(out)
    standard_bytes.append(out.encode("utf8"))
    non_standard_str.append(out_ns)
    non_standard_bytes.append(out_ns.encode("utf8"))

standard_map_bytes: dict[bytes, bytes] = dict(zip(
    non_standard_bytes, standard_bytes,
))
standard_map_str: dict[str, str] = dict(zip(
    non_standard_str, standard_str,
))
UNICODE_LOWER_RANGE: int = 0x0020
UNICODE_UPPER_RANGE: int = 0x02ff
SUPPORTED_RANGE: list[str] = [
    chr(i)
    for i in range(UNICODE_LOWER_RANGE, UNICODE_UPPER_RANGE+1)
    if chr(i)
]
UNICODE_COMBINING_LOWER_RANGE = 0x0300
UNICODE_COMBINING_UPPER_RANGE = 0x036f
combining_full: set[str] = {
    chr(i) for i in range(
    UNICODE_COMBINING_LOWER_RANGE, UNICODE_COMBINING_UPPER_RANGE+1)
}
# removes 4 combining from greek range
combining_full.remove(chr(0x0342))
combining_full.remove(chr(0x0343))
combining_full.remove(chr(0x0344))
combining_full.remove(chr(0x0345))

with open("latin.py", "w") as file:
    file.write("### GENERATED AUTOMATICALLY ###\n")
    # file.write("from re import Pattern, compile\n\n")
    # for debug purpose and eventual future use
    # file.write("STANDARD_STR: list[str] = [\n")
    # for i in standard_str:
    #     file.write(f'\t"{i}",\n')
    # file.write("]\n")
    # file.write("STANDARD_BYTES: list[bytes] = [\n")
    # for i in standard_bytes:
    #     file.write("\t{!r},\n".format(i))
    # file.write("]\n")
    # file.write("NON_STANDARD_STR: list[str] = [\n")
    # for i in non_standard_str:
    #     file.write(f'\t"{i}",\n')
    # file.write("]\n")
    # file.write("NON_STANDARD_BYTES: list[bytes] = [\n")
    # for i in non_standard_bytes:
    #     file.write("\t{!r},\n".format(i))
    # file.write("]\n")
    file.write("STANDARD_MAP_BYTES: dict[bytes, bytes] = {\n")
    for k, v in standard_map_bytes.items():
        file.write("\t{!r}: {!r},\n".format(k, v))
    file.write("}\n")

    file.write("STANDARD_MAP_STR: dict[str, str] = {\n")
    for k, v in standard_map_str.items():
        file.write("\t{!r}: {!r},\n".format(k, v))
    file.write("}\n")

    file.write("COMBINING_SUPPORTED: set[str] = {\n")
    for i in combining_supported:
        file.write(f'\t"{i}",\n')
    file.write("}\n")

    file.write("COMBINING_FULL: set[str] = {\n")
    for i in combining_full:
        file.write(f'\t"{i}",\n')
    file.write("}\n")

    # file.write('p: list[bytes] = [i.encode("utf8") for i in COMBINING_SUPPORTED]\n')
    # file.write('PATTERN: Pattern = compile(b"|".join(p))\n')
    file.write("SUPPORTED_RANGE: set[str] = {\n")
    for i in SUPPORTED_RANGE:
        # for debug purposes
        # if i == '"':
        #     file.write(f"\t'{hex(ord(i))}: {i}',\n")
        # elif i == "\\":
        #     file.write(f"\t'{hex(ord(i))}: \{i}',\n")
        # else:
        #     file.write(f'\t"{hex(ord(i))}: {i}",\n')
        if i == '"':
            file.write(f"\t'{i}',\n")
        elif i == "\\":
            file.write(f"\t'\{i}',\n")
        else:
            file.write(f'\t"{i}",\n')
    file.write("}\n")
