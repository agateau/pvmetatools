import shutil
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

TEST_VIDEO_PATH = DATA_DIR / "PXL_20240425_064525642.mp4"
TEST_PHOTO_PATH = DATA_DIR / "PXL_20240303_104151969.jpg"
NO_METADATA_PHOTO_PATH = DATA_DIR / "no_metadata.jpg"
NO_SUBSEC_PHOTO_PATH = DATA_DIR / "no_subsec_tag.jpg"

TEST_PATHS_AND_EXPECTED_NAMES: dict[Path, str] = {
    TEST_VIDEO_PATH: "2024-04-25_08-45-27.mp4",
    TEST_PHOTO_PATH: "2024-03-03_11-41-51.969.jpg",
    NO_SUBSEC_PHOTO_PATH: "2013-05-20_11-30-23.jpg",
    DATA_DIR / "panasonic_seqnum.jpg": "2014-06-07_19-51-53.867_n005.jpg",
}

EXPECTED_NAMES = list(TEST_PATHS_AND_EXPECTED_NAMES.values())


def copy_test_files(dst_path: Path) -> None:
    for path in TEST_PATHS_AND_EXPECTED_NAMES.keys():
        shutil.copy(path, dst_path)
