import re
from datetime import timedelta


class InvalidDeltaError(Exception):
    pass


def parse_delta(txt):
    delta = {}

    VALUE_RE = re.compile("[-+]?\d+")
    QUANTIFIER_RE = re.compile("[hms]")

    pos = 0
    while True:
        match = VALUE_RE.match(txt[pos:])
        if not match:
            break
        value = match.group(0)
        pos += len(value)

        match = QUANTIFIER_RE.match(txt[pos:])
        if not match:
            raise InvalidDeltaError("Invalid delta '%s', column %d"
                                    % (txt, pos + 1))
        quantifier = match.group(0)
        pos += len(quantifier)

        delta[quantifier] = int(value)

    if not delta:
        raise InvalidDeltaError("Invalid delta '%s'" % txt)

    return timedelta(
        hours=delta.get("h", 0),
        minutes=delta.get("m", 0),
        seconds=delta.get("s", 0),
        )
