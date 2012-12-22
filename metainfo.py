import subprocess

from datetime import datetime, timedelta


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


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
    cmd = ["avconv", "-v", "0", "-i", in_filename, "-metadata"]

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
    out = subprocess.Popen( \
        ["avprobe", "-show_format", filename], \
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) \
        .communicate()[0]

    dct = {}
    for line in out.splitlines():
        if line[0] == "[":
            continue
        key, value = line.strip().split("=", 1)
        if key.startswith("TAG:"):
            key = key[4:]
        dct[key] = value
    return dct
