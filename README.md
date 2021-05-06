## fix_enconding

Simple detection and fix for utf-8 strings that uses combining diacritical marks instead of native corresponding characters.


## What are diacritical marks ?

´ ` ˆ for example


## What are combining diacritical marks?

Special unicode characters that combines with others
```python
# Example for "combining" version
>>> s = "é"
>>> len(s)
2
>>> s.encode("utf8")
b"e\xcc\x81"

# Example for "native" version
>>> s = "é"
>>> len(s)
1
>>> s.encode("utf8")
b"\xc3\xa9"
```


## Why should I care?

You shouldn't really, but the use of combining diacritical marks can lead to 
buggy or invalid filenames, depending on your OS, software and unicode support.


## Installation

Use setup.py
```bash
python3 setup.py install
```


## Usage

```python
from fix_encoding import FixEncoding

latin_utf8_string = "thÌȘ īs ă tȄšt"
fixEncoding = FixEncoding(latin_utf8_string)

# detection of combining diacritical marks
if fixEncoding.containsCombining():
    # a native candidate exists for subtitution ?
    if fixEncoding.isFixable():
        fixed_string = fixEncoding.fix()
    else:
        # prints a list of non-substituable characters
        print(fixEncoding.getNonSubtituable())

# convinient iteration over graphemes
for grapheme in fixEncoding:
    print(grapheme)
```


## What's next?

CLI utils and support for non-latin language (Greek, Cyrillic, Japanese..)


## Notes

I included the module-generating code (./build_latin_index) for documentation purposes. Not needed to install the package.


## License

[GPLv2](https://choosealicense.com/licenses/gpl-2.0/)
