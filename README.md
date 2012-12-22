# avmeta-read

`avmeta-read <file> [<keyword>]`

Print meta information for `file`. Print all meta information if `keyword` is
not set.

# avmeta-write

`avmeta-write <file> <keyword>=<value>`

Set meta information for `file`. Multiple <keyword>=<value> arguments are
accepted. Original file is renamed to `file.orig`.

# avmeta-adjust-time

`avmeta-adjust-time <delta> <file1> [<file2>...]`

Adjust creation time of one or more files. `delta` is made of a sign, a value
and a quantifier. For example "+1h" "-2m"

# avmeta-time-rename

`avmeta-time-rename <file> [<file2>...]`

Rename files based on creation date, if available.
