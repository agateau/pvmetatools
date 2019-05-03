from datetime import datetime

import pyexiv2

DATE_TAGS = ('Exif.Image.DateTime',
             'Exif.Photo.DateTimeOriginal',
             'Exif.Image.DateTimeOriginal',
             'Exif.Photo.DateTimeDigitized')

SUBSEC_TAGS = ('Exif.Photo.SubSecTime',
               'Exif.Photo.SubSecTimeOriginal',
               'Exif.Photo.SubSecTimeDigitized')


def name_from_metadata(image_name):
    metadata = pyexiv2.ImageMetadata(image_name)
    metadata.read()

    # Find a valid date
    date = None
    for tag_name in DATE_TAGS:
        try:
            date_tag = metadata[tag_name]
        except KeyError:
            continue
        date = date_tag.value
        if not isinstance(date, datetime):
            continue
        break
    else:
        raise Exception("No date tag found")

    subsec = None
    for tag_name in SUBSEC_TAGS:
        try:
            subsec_tag = metadata[tag_name]
        except KeyError:
            continue
        subsec = subsec_tag.value
        break

    try:
        sequence_tag = metadata['Exif.Panasonic.SequenceNumber']
        sequence = sequence_tag.value
    except KeyError:
        sequence = None

    new_name = date.strftime("%Y-%m-%d_%H-%M-%S")
    if subsec is not None:
        new_name += ".{}".format(subsec)
    if sequence is not None:
        new_name += "_n{:03}".format(sequence)

    return new_name
# vi: ts=4 sw=4 et
