from pathlib import Path

import pytest
from data import NO_METADATA_PHOTO_PATH, TEST_PHOTO_PATH

from pvmetatools import photorename


def test_name_from_metadata():
    name = photorename.name_from_metadata(str(TEST_PHOTO_PATH))
    assert name == "2024-03-03_11-41-51.969"


def test_name_from_metadata_invalid_image(tmp_path: Path):
    invalid_path = tmp_path / "invalid.jpg"

    content = TEST_PHOTO_PATH.read_bytes()[:40]
    invalid_path.write_bytes(content)

    with pytest.raises(OSError):
        photorename.name_from_metadata(str(invalid_path))


def test_name_from_metadata_no_date():
    with pytest.raises(RuntimeError, match="No date tag found"):
        photorename.name_from_metadata(str(NO_METADATA_PHOTO_PATH))
