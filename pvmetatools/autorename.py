#!/usr/bin/env python3
import argparse
import functools
import os
import re
import sys
from typing import Iterator

from pvmetatools import photorename, videorename

DESCRIPTION = """\
Renames photos and videos according to the date and time encoded in their meta
data.
"""


PHOTO_EXTS = {".jpeg", ".jpg", ".cr2"}


def ensure_unique(original_filepath: str, new_name_we: str, ext: str) -> str | None:
    """Return a unique filepath for original_filepath, based on new_name_we and
    ext, or None if the file does not need to be renamed"""

    # If new filepath is the same as old filepath, no need to rename
    filedir = os.path.dirname(original_filepath)
    new_filepath = os.path.join(filedir, new_name_we + ext)
    if new_filepath == original_filepath:
        return None

    # If original name without _dupNNN suffix is the same as new_name, no need
    # to rename
    original_name_we = os.path.splitext(os.path.basename(original_filepath))[0]
    match = re.match(r"^(.+?)_dup\d{3,}$", original_name_we)
    if match and match.group(1) == new_name_we:
        return None

    count = 1
    while os.path.exists(new_filepath):
        new_filepath = os.path.join(
            filedir, "{}_dup{:03}{}".format(new_name_we, count, ext)
        )
        count += 1
    return new_filepath


def create_new_name(filepath: str, timezone: str) -> str | None:
    ext = os.path.splitext(filepath)[1].lower()
    if ext in PHOTO_EXTS:
        name_fcn = photorename.name_from_metadata
    else:
        name_fcn = functools.partial(videorename.name_from_metadata, timezone=timezone)

    new_name = name_fcn(filepath)
    return ensure_unique(filepath, new_name, ext)


def read_from_stdin() -> Iterator[str]:
    for line in sys.stdin:
        line = line.strip()
        if not line or line[0] == "#":
            continue
        yield line


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.description = DESCRIPTION

    parser.add_argument("-n", "--dry-run", action="store_true", help="Simulate")

    parser.add_argument(
        "--tz",
        metavar="TIMEZONE",
        default="local",
        help="The timezone to use for videos. Defaults to the local timezone.",
    )

    parser.add_argument(
        "files", nargs="+", help="Files to rename. Use - to read them from stdin"
    )

    args = parser.parse_args(argv)

    if args.files == ["-"]:
        filepaths = read_from_stdin()
    else:
        filepaths = iter(args.files)

    for filepath in filepaths:
        try:
            new_filepath = create_new_name(filepath, args.tz)
        except Exception as exc:
            print("{}: fail: {}".format(filepath, exc))
            continue

        if new_filepath is None:
            continue

        print("{} -> {}".format(filepath, new_filepath))
        if not args.dry_run:
            os.rename(filepath, new_filepath)

    return 0


# vi: ts=4 sw=4 et
