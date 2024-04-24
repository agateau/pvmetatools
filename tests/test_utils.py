from datetime import timedelta

import pytest

from pvmetatools.utils import parse_delta


@pytest.mark.parametrize(
    "txt,delta",
    [
        ("-12h", timedelta(hours=-12)),
        ("2h-3m+4s", timedelta(hours=2, minutes=-3, seconds=4)),
    ],
)
def test_parse_delta(txt, delta):
    result = parse_delta(txt)
    assert result == delta
