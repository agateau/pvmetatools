import os
from pathlib import Path

import pytest
from data import DATA_DIR, TEST_PHOTO_PATH, TEST_VIDEO_PATH

from pvmetatools import autorename


@pytest.mark.parametrize(
    "original_name,new_name,dir_content,expected",
    [
        # No rename
        ("bob.jpg", "1234.jpg", ("5678.jpg",), "1234.jpg"),
        # Normal rename
        ("bob.jpg", "1234.jpg", ("1234.jpg",), "1234_dup001.jpg"),
        # First dup already exists
        ("bob.jpg", "1234.jpg", ("1234.jpg", "1234_dup001.jpg"), "1234_dup002.jpg"),
        # First dup already exists, but original name was first dup
        ("1234_dup001.jpg", "1234.jpg", ("1234.jpg", "1234_dup001.jpg"), None),
        (
            "2004-04-13_12-29-00.jpg",
            "2004-04-13_12-29-00.jpg",
            ("2004-04-13_12-29-00.jpg",),
            None,
        ),
    ],
)
def test_ensure_unique(
    tmpdir: str,
    original_name: str,
    new_name: str,
    dir_content: list[str],
    expected: str | None,
) -> None:
    for name in dir_content:
        path = os.path.join(tmpdir, name)
        open(path, "w").close()

    result = autorename.ensure_unique(
        os.path.join(tmpdir, original_name), *os.path.splitext(new_name)
    )

    if expected is None:
        assert result is None
    else:
        assert result == os.path.join(tmpdir, expected)


@pytest.mark.parametrize(
    "original_path,new_name",
    [
        (TEST_VIDEO_PATH, "2024-04-25_08-45-27.mp4"),
        (TEST_PHOTO_PATH, "2024-03-03_11-41-51.969.jpg"),
    ],
)
def test_create_new_name(original_path: Path, new_name: str) -> None:
    result = autorename.create_new_name(str(original_path))
    expected = str(DATA_DIR / new_name)
    assert result == expected
