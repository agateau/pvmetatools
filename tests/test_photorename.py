from data import TEST_PHOTO_PATH

from pvmetatools import photorename


def test_name_from_metadata():
    name = photorename.name_from_metadata(str(TEST_PHOTO_PATH))
    assert name == "2024-03-03_11-41-51.969"
