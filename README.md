# pvmetatools

Tools to manage metainfo and filenames in photos and videos.

## Installation

```
pipx install https://github.com/agateau/pvmetatools
```

## Available tools

### pvmeta-photo-autorename

Rename pictures according to their EXIF information, taking sequence number into account.

This relies on the presence of the EXIF.Panasonic.SequenceNumber tag, so may not work with all cameras.

### pvmeta-video-metaread

`pvmeta-video-metaread <file> [<keyword>]`

Print meta information for `file`. Print all meta information if `keyword` is not set.

### pvmeta-video-metawrite

`pvmeta-video-metawrite <file> <keyword>=<value>`

Set meta information for `file`. Multiple `<keyword>=<value>` arguments are accepted. Original file is renamed to `file.orig`.

### pvmeta-video-adjusttime

`pvmeta-video-adjusttime <delta> <file1> [<file2>...]`

Adjust creation time of one or more files. `delta` is made of a sign, a value and a quantifier. For example "1h", "2m", "2m-30s"

### pvmeta-video-timerename

`pvmeta-video-timerename <file> [<file2>...]`

Rename files based on creation date, if available.

## Running tests

```
pip install -r dev-requirements.txt
pytest
```
