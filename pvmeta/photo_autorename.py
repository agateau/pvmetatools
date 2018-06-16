#!/usr/bin/env python
import os
import sys
from datetime import datetime
from optparse import OptionParser

import pyexiv2

USAGE = "%prog [options] <pict1> [<pict2>...]"

DATE_TAGS = ('Exif.Image.DateTime',
             'Exif.Photo.DateTimeOriginal',
             'Exif.Image.DateTimeOriginal',
             'Exif.Photo.DateTimeDigitized')


def name_from_metadata(image_name):
    adir = os.path.dirname(image_name)
    metadata = pyexiv2.ImageMetadata(image_name)
    metadata.read()

    # Find a valid date
    date = None
    for tag_name in DATE_TAGS:
        try:
            date_tag = metadata[tag_name]
        except KeyError:
            continue
        date = date_tag.value
        if not isinstance(date, datetime):
            continue
        break
    else:
        raise Exception("No date tag found")

    try:
        sequence_tag = metadata['Exif.Panasonic.SequenceNumber']
        sequence = sequence_tag.value
    except KeyError:
        sequence = 0

    new_name = date.strftime("%Y-%m-%d_%H-%M-%S")
    if sequence > 0:
        new_name += "-n%03d" % sequence

    count = 0
    while True:
        full_name = os.path.join(adir, new_name)
        if count > 0:
            full_name += "_%d" % count
        full_name += ".jpg"
        if full_name == image_name or not os.path.exists(full_name):
            return full_name
        count += 1


def main():
    parser = OptionParser(usage=USAGE)
    parser.add_option("--dry-run",
                      action="store_true", dest="dry_run", default=False,
                      help="Dry run, print what would be done")

    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("Missing args")

    for name in sorted(args):
        print("%s:" % name, end=' ')
        try:
            new_name = name_from_metadata(name)
        except Exception as exc:
            print("failure")
            print(exc)
            continue
        if new_name == name:
            print("no change")
        else:
            print("-> %s" % new_name)
            if not options.dry_run:
                assert not os.path.exists(new_name)
                os.rename(name, new_name)

    return 0


if __name__ == "__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
