from datetime import timedelta

import arrow
from approx import Approx
from data import TEST_VIDEO_PATH

from pvmetatools import metainfo


def test_read():
    dct = metainfo.read(str(TEST_VIDEO_PATH))

    creation_time = arrow.get("2024-04-25T08:45:27+02:00")

    assert dct == {
        "filename": str(TEST_VIDEO_PATH),
        "nb_streams": 2,
        "nb_programs": 0,
        "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
        "format_long_name": "QuickTime / MOV",
        "start_time": "0.000000",
        "duration": Approx(
            timedelta(microseconds=589_000),
            timedelta(microseconds=590_000),
        ),
        "size": 1228124,
        "bit_rate": Approx(16_664_000, 16_667_000),
        "probe_score": 100,
        "major_brand": "isom",
        "minor_version": "131072",
        "compatible_brands": "isomiso2mp41",
        "creation_time": creation_time,
        "com.android.capture.fps": "30.000000",
    }
