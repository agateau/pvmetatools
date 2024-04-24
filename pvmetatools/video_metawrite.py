#!/usr/bin/env python3
import os
import sys
from optparse import OptionParser
from typing import Iterable

from pvmetatools import metainfo

USAGE = "%prog <file> <keyword>=<value> [<keyword>=<value>...]"


def parse_keywords(args: Iterable[str]) -> dict[str, str]:
    dct = {}
    for arg in args:
        key, value = arg.split("=", 1)
        dct[key] = value
    return dct


def main():
    parser = OptionParser(usage=USAGE)
    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.error("Missing args")

    name = args[0]

    dct = parse_keywords(args[1:])

    tmpname = "tmp-" + name
    metainfo.write(name, tmpname, dct)

    os.rename(name, name + ".orig")
    os.rename(tmpname, name)

    return 0


if __name__ == "__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
