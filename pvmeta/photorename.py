from datetime import datetime

import pyexiv2

DATE_TAGS = ('Exif.Image.DateTime',
             'Exif.Photo.DateTimeOriginal',
             'Exif.Image.DateTimeOriginal',
             'Exif.Photo.DateTimeDigitized')


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

    try:
        sequence_tag = metadata['Exif.Panasonic.SequenceNumber']
        sequence = sequence_tag.value
    except KeyError:
        sequence = 0

    new_name = date.strftime("%Y-%m-%d_%H-%M-%S")
    if sequence > 0:
        new_name += "_n{:03}".format(sequence)

    return new_name
# vi: ts=4 sw=4 et
