from re import Pattern, Match, compile
from typing import Any, Optional

"""
All data comes from https://www.utf8-chartable.de/
LATIN
Data extraction valid for combining.csv (U+0300 - U+036F) 
are excluded U+0342, U+0343, U+0344, U+0345 : Greek support will be done in a separate extension
combining 1 diacritical mark
"""

p: str = r"COMBINING\s(.*)"
pattern: Pattern = compile(p)
letter: str
description: str
r: Optional[Match[str]]
_: str
results: list[tuple[Any, ...]] = []

def main() -> list[tuple[Any, ...]]:
    with open("combining.csv", "r") as f:
        raw = f.read()

    for row in raw.split("\n")[:-1]:    
        try:
            _, letter, _, description = row.split("\t")
            r = pattern.search(description)
            results.append(
                (letter, r.group(1))
            )

        except ValueError as err:
            print("Inconistent spacing:")
            print(row)
            raise

        except AttributeError as err:
            print(f"Regex returned {r}:")
            print(row)

    return results    
