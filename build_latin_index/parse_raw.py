from re import Pattern, Match, compile
from typing import Any, Optional

"""
All data comes from https://www.utf8-chartable.de/
LATIN 
Data extraction valid for raw.csv (U+0000 - U+02AF)
"""

p: str = r"^LATIN\s((SMALL|CAPITAL)\sLETTER)\s([A-Z]{1,6}(?=\sWITH\s))\sWITH\s(.*)$"
pattern: Pattern = compile(p)

letter: str
description: str
r: Optional[Match[str]]
_: str
results: list[tuple[Any, ...]] = []

def main() -> list[tuple[Any, ...]]:
    with open("raw.csv", "r") as f:
        raw = f.read()

    for row in raw.split("\n")[:-1]:
        try:
            _, letter, _, description = row.split("\t")
            r = pattern.search(description)
            results.append(
                (r.group(1), r.group(3), r.group(4), letter)
            )

        except ValueError as err:
            print("Inconistent spacing:")
            print(row)
            raise

        except AttributeError as err:
            print(f"Regex returned {r}:")
            print(row)
    
    return results
