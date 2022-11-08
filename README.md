# Pvmetatools

Pvmetatools (Photo Video Metadata Tools) lets you manipulate metadata and filenames of photo and video files.

## Installation

The simplest way to install it is to use [pipx](https://pypa.github.io/pipx/):

```
pipx install https://github.com/agateau/pvmetatools
```

[FFmpeg][] binaries (`ffmpeg`, `ffprobe`) are required to manipulate video files.

[FFmpeg]: https://ffmpeg.org/

## Available tools

### pvmeta-autorename

Rename photo and video files using the date stored in their metadata.

Photos are renamed according to their EXIF information, taking sequence number into account. This relies on the presence of the `EXIF.Panasonic.SequenceNumber` tag, so may not work with all cameras.

### pvmeta-video-metaread

`pvmeta-video-metaread <file> [<keyword>]`

Print metadata for `file`. Print all metadata if `keyword` is not set.

### pvmeta-video-metawrite

`pvmeta-video-metawrite <file> <keyword>=<value>`

Set metadata for `file`. Multiple `<keyword>=<value>` arguments are accepted. The original file is renamed to `file.orig`.

### pvmeta-video-adjusttime

`pvmeta-video-adjusttime <delta> <file1> [<file2>...]`

Adjust the creation time of one or more files. `delta` is made of a sign, a value and a quantifier. For example "1h", "2m", "2m-30s"

## Working on the project

The project is developed using [Poetry](https://python-poetry.org/):

```
# Open a shell
poetry shell

# Install the app and its dependencies
poetry install

# Run tests
pytest
```
