import json
import subprocess
from datetime import timedelta
from typing import Any, Callable

import arrow

FFMPEG_BINARY = "ffmpeg"
PROBE_BINARY = "ffprobe"


ProcessFn = Callable[[str], Any]


def read(filename: str) -> dict[str, Any]:
    info = _run_avprobe(filename)

    processors: dict[str, ProcessFn] = {
        "creation_time": _process_time,
        "duration": _process_duration,
        "bit_rate": _process_int,
        "size": _process_int,
    }

    for key, fcn in processors.items():
        if key in info:
            info[key] = fcn(info[key])
    return info


def write(in_filename: str, out_filename: str, keywords: dict[str, str]) -> None:
    cmd = [FFMPEG_BINARY, "-v", "0", "-i", in_filename, "-metadata"]

    for key, value in keywords.items():
        cmd.append("%s=%s" % (key, value))

    cmd.extend(["-codec", "copy"])

    cmd.append(out_filename)
    subprocess.check_call(cmd)


def _process_duration(txt: str) -> timedelta:
    return timedelta(seconds=float(txt))


def _process_int(txt: str) -> int:
    return int(txt.split(".")[0])


def _process_time(txt: str) -> arrow.Arrow:
    return arrow.get(txt).to("local")


def _run_avprobe(filename: str) -> dict[str, Any]:
    out = subprocess.check_output(
        [PROBE_BINARY, "-of", "json", "-show_format", filename],
        stderr=subprocess.DEVNULL,
    )
    out = out.decode("utf-8")

    # Return the "format" dict, but flatten the "tags" subdict into it
    dct = json.loads(out)["format"]
    tag_dct = dct.pop("tags")
    dct.update(tag_dct)
    return dct
