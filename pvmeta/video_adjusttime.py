#!/usr/bin/env python3
import os
import sys
from optparse import OptionParser

from pvmeta import metainfo
from pvmeta import utils


USAGE = "%prog <delta> <file1> [<file2>...]"


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def adjust_time(name, delta):
    dct = metainfo.read(name)
    date = dct["creation_time"] + delta

    keywords = {"creation_time": date.strftime(DATETIME_FORMAT)}

    tmpname = "tmp-" + name
    metainfo.write(name, tmpname, keywords)

    os.rename(name, name + ".orig")
    os.rename(tmpname, name)


def main():
    parser = OptionParser(usage=USAGE)
    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.error("Missing args")

    try:
        delta = utils.parse_delta(args[0])
    except utils.InvalidDeltaError as exc:
        print(exc)
        print("Valid delta values: '1h', '2m', '2m-30s'")
        return 1

    for name in args[1:]:
        print("Processing `%s`" % name)
        if not os.path.exists(name):
            print("ERROR: File does not exist")
            return 1
        adjust_time(name, delta)

    return 0


if __name__ == "__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
