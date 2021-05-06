# import fix_encoding.latin as latin
from . import latin
from . import japanese
from . import merge

def type_check(fnc):
    def inner(self, s: str):
        for k, v in fnc.__annotations__.items():
            if not isinstance(locals()[k], v):
                raise TypeError(f"Expected parameter of type: {v}")
        return fnc(self, s)
    return inner
            

class FixEncoding(object):

    @type_check
    def __init__(self, s: str):
        self.s: str = s
        self.unique_individual_symbols: set[str] = set(s)
        language: str = ""
        self.COMBINING_SUPPORTED: set[str]
        self.COMBINING_FULL: set[str]
        self.SUPPORTED_RANGE: set[str]
        self.STANDARD_MAP_BYTES: dict[bytes, bytes]
        self.STANDARD_MAP_STR: dict[str, str]
        # NOT_IMPLEMENTED: U+0370 - U+2FA1E

        # only latin range is supported yet (U+0000 - U+036F)
        mixed_japanese = latin.SUPPORTED_RANGE | latin.COMBINING_FULL | japanese.SUPPORTED_RANGE | japanese.COMBINING_FULL
        if not (self.unique_individual_symbols - (latin.SUPPORTED_RANGE | latin.COMBINING_FULL)):
            language = "latin"
        elif not (self.unique_individual_symbols - (japanese.SUPPORTED_RANGE | japanese.COMBINING_FULL)):
            language = "japanese"
        elif not (self.unique_individual_symbols - (merge.SUPPORTED_RANGE | merge.COMBINING_FULL)):
            language = "merge"
        else:
            print(self.unique_individual_symbols - mixed_japanese)
            raise NotImplementedError("Non latin character detected")

        # dynamically inject module's namespace in class's according to detected unicode range
        self.__dict__.update(globals()[language].__dict__)
        # self.lang = globals()[language]
        self.individual_characters: list[str] = [ i for i in self ]
        self.unique_individual_characters: set[str] = { i for i in self }

    def containsCombining(self) -> bool:
        """verifies the string passed to __init__ contains combining diacritical mark(s)"""
        if (self.unique_individual_symbols & self.COMBINING_SUPPORTED):
            return True
        return False
    
    def isFixable(self) -> bool:
        """verifies the string passed to __init__ contains only substituable grapheme(s)"""
        unique_diacritics: set[str] = self.unique_individual_characters - self.SUPPORTED_RANGE
        if(unique_diacritics - self.STANDARD_MAP_STR.keys()):
            return False
        return True

    def getDiacritics(self) -> list[str]:
        """returns grapheme(s) with combining diacritics contained in the string passed to __init__"""
        buffer: list[str] = []
        for s in self.individual_characters:
            if (set(s) & self.COMBINING_FULL):
                buffer.append(s)
        return buffer

    def getNonSubtituable(self) -> list[str]:
        """returns non-subtituable grapheme(s)"""
        unique_diacritics: set[str] = self.unique_individual_characters - self.SUPPORTED_RANGE
        return list(unique_diacritics - self.STANDARD_MAP_STR.keys())

    def fix(self) -> str:
        """substitutes grapheme(s) that uses combining diacritical mark(s) for native version"""
        if not self.isFixable():
            message = "String contains non-substituable characters:\n"
            message = f"{message}{self.getNonSubtituable()}"
            raise ValueError(message)

        r: list[str] = []
        for s in self.individual_characters:
            r.append(self.STANDARD_MAP_STR.get(s, s) )
        return "".join(r)

    def __iter__(self):
        self.n: int = 0
        self.max = len(self.s)
        return self

    # ToDO: rendre l'itérateur compatible avec TOUS les combining de TOUS les languages
    def __next__(self) -> str:
        """iterates over string according to grapheme(s)"""
        buffer: list[str] = []
        if self.n >= self.max:
            raise StopIteration
        try:
            buffer.append(self.s[self.n])
            while (self.s[self.n+1] in self.COMBINING_FULL):
                buffer.append(self.s[self.n+1])
                self.n += 1
        except IndexError:
            pass
        finally:
            self.n += 1
            return "".join(buffer)

    def __len__(self):
        """returns number of grapheme(s) in string passed to __init__"""
        return len(self.individual_characters)
