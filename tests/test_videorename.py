from data import TEST_VIDEO_PATH, TIMEZONE

from pvmetatools import videorename


def test_name_from_metadata():
    name = videorename.name_from_metadata(str(TEST_VIDEO_PATH), TIMEZONE)
    assert name == "2024-04-25_08-45-27"
