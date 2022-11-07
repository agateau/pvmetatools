from pvmeta import metainfo


def name_from_metadata(video_name):
    dct = metainfo.read(video_name)
    date = dct["creation_time"]
    return date.strftime("%Y-%m-%d_%H-%M-%S")
# vi: ts=4 sw=4 et
