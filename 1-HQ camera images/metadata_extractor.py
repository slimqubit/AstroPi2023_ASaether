from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
from GPSPhoto import gpsphoto

import csv


# create .csv file
header = ['Name', 'Coordinates', 'Date & Time']
with open('image_data.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)


    for idx in range(0,537):
        image_string = "image" + str(idx) + ".jpg"

        # open the image
        image = Image.open(image_string)

        # extracting the exif metadata
        exif_table={}
        for k, v in image.getexif().items():
            tag=TAGS.get(k)
            # obtain date & time info
            if tag=="DateTime":
                date_time=v

        # obtain GPS info
        gps = gpsphoto.getGPSData(image_string)
        gps_string = str(gps['Latitude']) + ' ' + str(gps['Longitude'])

        # write data in .csv file
        dataset = [image_string, gps_string, date_time]
        writer.writerow(dataset)
