import Image
from ExifTags import TAGS
import sys
import os
import glob
from random import randint
import shutil
import time

def getExif(image):
    """ get exif meta data from image
    """
    metas = {}
    try:
        img = Image.open(image)
    except IOError:
        print "*WARN* invalid photo type  " + str(image)
        return None
    info = img._getexif()
    if info is None:
        print "*WARN* no EXIF information of " + str(image)
        return None
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        metas[decoded] = value
    return metas

def sortPhotos(src_path, dst_path):
    """ sort photos according to its EXIF date time. renamed them using its
    EXIF date time, like 'IMG_20121018101213100.JPG'
    @src_path: source photos' path
    @dst_path: destination of photos sorted
    """
    if not os.path.exists(src) or not os.path.exists(dst):
        print "*ERROR* invalid directory."

    photos = []
    invalid_photos = []
    photos_with_limit_exif = []
    extensions = ['.JPG', '.jpg']
    for path, dirs, files in os.walk(src_path):
        for each in files:
            if os.path.splitext(each)[1] in extensions:
                photos.append(os.path.abspath(path) + os.path.sep + each)
    print photos

    for photo in photos:
        info = getExif(photo)
        if info is None:
            invalid_photos.append(photo)
            continue
        if not info.has_key('DateTime'):
            print "*WARN* invalid EXIF meta data of " + photo
            photos_with_limit_exif.append(photo)
            continue
        date_time = info['DateTime']
        date_dir = date_time.split()[0].split(':')[0]
        date_in_name = ''.join(date_time.split()).replace(':', '')
        suffix = str(randint(100, 199))
        ext = os.path.splitext(photo)[1]
        photo_name = "IMG_" + date_in_name + suffix + ext
        dir_name = os.path.abspath(dst_path) + os.path.sep + date_dir
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        print 'copy: %s --> %s' % (photo, dir_name+os.path.sep+photo_name)
        shutil.copy2(photo, dir_name+os.path.sep+photo_name)

    for photo in photos_with_limit_exif:
        last_changed_time = time.localtime(os.path.getctime(photo))
        date_dir = time.strftime("%Y")
        date_in_name =  time.strftime("%Y%m%d%H%M%S", last_changed_time)
        suffix = str(randint(100, 199))
        ext = os.path.splitext(photo)[1]
        photo_name = "IMG_" + date_in_name + suffix + ext
        dir_name = os.path.abspath(dst_path) + os.path.sep + date_dir
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        print 'copy: %s --> %s' % (photo, dir_name+os.path.sep+photo_name)
        shutil.copy2(photo, dir_name+os.path.sep+photo_name)

    print 'Total photos: ' + str(len(photos))
    print 'Total photos with limit exif: ' + str(len(photos_with_limit_exif))

if __name__ == '__main__':
    if len(sys.argv) == 3:
        src = sys.argv[1]
        dst = sys.argv[2]
        print "sorting photos from %s to %s." % (src, dst)
        sortPhotos(src, dst)
    else:
        print "*ERROR* please input src path and dst path"

