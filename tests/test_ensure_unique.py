import os

import pytest

from pvmetatools.autorename import ensure_unique


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

    result = ensure_unique(
        os.path.join(tmpdir, original_name), *os.path.splitext(new_name)
    )

    if expected is None:
        assert result is None
    else:
        assert result == os.path.join(tmpdir, expected)
