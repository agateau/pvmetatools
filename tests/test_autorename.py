import os
from pathlib import Path

import data
import pytest

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


@pytest.mark.parametrize("original_path,new_name", data.TEST_PATHS_AND_EXPECTED_NAMES)
def test_create_new_name(original_path: Path, new_name: str) -> None:
    result = autorename.create_new_name(str(original_path))
    expected = str(data.DATA_DIR / new_name)
    assert result == expected


def test_main_happy_path(tmp_path: Path) -> None:
    # GIVEN a set of test files
    data.copy_test_files(tmp_path)

    # WHEN autorename is called on them
    autorename.main([str(x) for x in tmp_path.glob("*")])

    # THEN they are properly renamed
    final_names = {x.name for x in tmp_path.glob("*")}
    assert final_names == set(data.EXPECTED_NAMES)


def test_main_already_renamed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # GIVEN a set of test files, already renamed
    data.copy_test_files(tmp_path)
    autorename.main([str(x) for x in tmp_path.glob("*")])
    captured = capsys.readouterr()

    assert " -> " in captured.out

    # WHEN autorename is called on them
    autorename.main([str(x) for x in tmp_path.glob("*")])
    captured = capsys.readouterr()

    # THEN nothing happens
    assert captured.out == ""
    final_names = {x.name for x in tmp_path.glob("*")}
    assert final_names == set(data.EXPECTED_NAMES)
