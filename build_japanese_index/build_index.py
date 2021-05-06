from template_katakana import katakana
from template_hiragana import hiragana
# U+3099	゙	e3 82 99	COMBINING KATAKANA-HIRAGANA VOICED SOUND MARK
# U+309A	゚	e3 82 9a	COMBINING KATAKANA-HIRAGANA SEMI-VOICED SOUND MARK
native = katakana + hiragana
# lookup_table_katakana: dict[str, str] = {}
# combining: list[tuple[Any, ...]] = []
# native: list[tuple[Any, ...]] = []
# combining_ = pc()
# native = pr()
# native_double = prd()
# lookup_table_combining: dict[str, str] = { k: v for (v, k) in combining_ }
standard_str: list[str] = []
standard_bytes: list[bytes] = []
non_standard_str: list[str] = []
non_standard_bytes: list[bytes] = []
dakuten = b"\xe3\x82\x99"
handakuten = b"\xe3\x82\x9a"

for base, *dia in native:
    standard_str.append(dia[0])
    standard_bytes.append(dia[0].encode("utf8"))
    non_standard_str.append(base + dakuten.decode("utf8"))
    non_standard_bytes.append(base.encode("utf8") + dakuten)
    if len(dia) == 2:
        standard_str.append(dia[1])
        standard_bytes.append(dia[1].encode("utf8"))
        non_standard_str.append(base + handakuten.decode("utf8"))
        non_standard_bytes.append(base.encode("utf8") + handakuten)

standard_map_bytes: dict[bytes, bytes] = dict(zip(
    non_standard_bytes, standard_bytes,
))
standard_map_str: dict[str, str] = dict(zip(
    non_standard_str, standard_str,
))

HALF_WIDTH_LOWER_RANGE = 0xff00
HALF_WIDTH_UPPER_RANGE = 0xff9f
FULL_WIDTH_LOWER_RANGE = 0x3040
FULL_WIDTH_UPPER_RANGE = 0x3100
KANJI_LOWER_RANGE = 0x4e00
KANJI_UPPER_RANGE = 0x9fff

SUPPORTED_RANGE: list[str] = [
    chr(i)
    for i in range(HALF_WIDTH_LOWER_RANGE, HALF_WIDTH_UPPER_RANGE+1)
    if chr(i)
]
for i in range(FULL_WIDTH_LOWER_RANGE, FULL_WIDTH_UPPER_RANGE):
    if chr(i):
        SUPPORTED_RANGE.append(chr(i))
for i in range(KANJI_LOWER_RANGE, KANJI_UPPER_RANGE+1):
    if chr(i):
        SUPPORTED_RANGE.append(chr(i))

combining_full: set[str] = {dakuten.decode("utf8"), handakuten.decode("utf8")}
combining_supported: set[str] = combining_full

with open("japanese.py", "w") as file:
    file.write("### GENERATED AUTOMATICALLY ###\n")

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
