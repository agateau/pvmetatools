#!/usr/bin/env python3
import sys
from optparse import OptionParser

from pvmeta import metainfo

USAGE = "%prog <file> [<keyword>]"


def main():
    parser = OptionParser(usage=USAGE)
    (options, args) = parser.parse_args()

    if len(args) == 0:
        parser.error("Missing args")

    dct = metainfo.read(args[0])

    if len(args) == 2:
        print(dct[args[1]])
    else:
        for key in sorted(dct.keys()):
            print("%s=%s" % (key, dct[key]))

    return 0


if __name__ == "__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
