from . import latin
from . import japanese

STANDARD_MAP_BYTES: dict[bytes, bytes] = latin.STANDARD_MAP_BYTES | japanese.STANDARD_MAP_BYTES
STANDARD_MAP_STR: dict[str, str] = latin.STANDARD_MAP_STR | japanese.STANDARD_MAP_STR
COMBINING_SUPPORTED: set[str] = latin.COMBINING_SUPPORTED | japanese.COMBINING_SUPPORTED
COMBINING_FULL: set[str] = latin.COMBINING_FULL | japanese.COMBINING_FULL
SUPPORTED_RANGE: set[str] = latin.SUPPORTED_RANGE | japanese.SUPPORTED_RANGE