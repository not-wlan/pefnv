import sys
import pefile
import fnv


class Export:
    def __init__(self, name: bytes, module: str):
        self.name = name
        self.module = module
        self.hash32 = self.hash(32)
        self.hash64 = self.hash(64)

    def __str__(self):
        return f"[{self.module}] {self.name}\n\t-> 32: {self.hash32}\n\t-> 64: {self.hash64}"

    def hash(self, bits=32):
        return fnv.hash(self.name, algorithm=fnv.fnv_1a, bits=bits)

    def match(self, other):
        return True if other.hash32 == self.hash32 or other.hash64 == self.hash64 else False


def find_dupes(exports):
    dupes = []
    for export in exports:
        found = [x for x in exports if export.match(x) and x.name != export.name]
        if len(found):
            dupes.append((export, found))
    return dupes


def main():
    files = sys.argv[1:]
    exports = []

    for arg in files:
        pe: pefile.PE = pefile.PE(arg)
        symbols = pe.DIRECTORY_ENTRY_EXPORT.symbols
        exports += [Export(export.name, arg) for export in symbols if export.name]

    print(f"named exports: {len(exports)}")
    exports += [Export(b'liquid', "test"), Export(b'costarring', "test")]
    dupes = find_dupes(exports)

    print(f"found {len(dupes)} dupes!")
    for dupe in dupes:
        print(f"{dupe[0]}")
        for match in dupe[1]:
            print(f"-> {match.name}")


if __name__ == '__main__':
    main()
