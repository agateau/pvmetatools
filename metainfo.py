import json
import subprocess

from datetime import datetime, timedelta


DATETIME_FORMAT = r"%Y-%m-%d %H:%M:%S"

FFMPEG_BINARY = "ffmpeg"
PROBE_BINARY = "ffprobe"


def read(filename):
    info = _run_avprobe(filename)

    processors = {
        "creation_time": _process_time,
        "duration": _process_duration,
        "bit_rate": _process_int,
        "size": _process_int,
    }

    for key, fcn in processors.items():
        if key in info:
            info[key] = fcn(info[key])
    return info


def write(in_filename, out_filename, keywords):
    cmd = [FFMPEG_BINARY, "-v", "0", "-i", in_filename, "-metadata"]

    for key, value in keywords.items():
        cmd.append("%s=%s" % (key, value))

    cmd.extend(["-codec", "copy"])

    cmd.append(out_filename)
    subprocess.check_call(cmd)


def _process_duration(txt):
    return timedelta(seconds=float(txt))


def _process_int(txt):
    return int(txt.split(".")[0])


def _process_time(txt):
    return datetime.strptime(txt, DATETIME_FORMAT)


def _run_avprobe(filename):
    out = subprocess.Popen(
        [PROBE_BINARY, "-of", "json", "-show_format", filename],
        stdout=subprocess.PIPE, stderr=open("/dev/null", "w")) \
        .communicate()[0]

    # Return the "format" dict, but flatten the "tags" subdict into it
    dct = json.loads(out)["format"]
    tag_dct = dct.pop("tags")
    dct.update(tag_dct)
    return dct
