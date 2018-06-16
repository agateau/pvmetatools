#!/usr/bin/env python3
import os
import sys
from optparse import OptionParser

from pvmeta import metainfo


USAGE = "%prog <file1> [<file2>...]"


def main():
    parser = OptionParser(usage=USAGE)
    parser.add_option("--dry-run",
                      action="store_true", dest="dry_run", default=False,
                      help="List changes, do not apply them")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("Missing args")

    for name in args:
        print("%s ->" % name, end=' ')
        dct = metainfo.read(name)
        date = dct["creation_time"]
        ext = os.path.splitext(name)[1]

        newname = date.strftime("%Y-%m-%d_%H-%M-%S") + ext
        print(newname)
        if not options.dry_run:
            dirname = os.path.dirname(name)
            fullnewname = os.path.join(dirname, newname)
            os.rename(name, fullnewname)

    return 0


if __name__ == "__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
