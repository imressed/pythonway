__author__ = 'Imressed'

from PIL import Image

global ext, cropped_name
ext = ".jpg"
cropped_name = "CROPPED"


def sort_parts(x_start, y_start, x_finish, y_finish, img_size):
    box = []
    if x_start < 0: x_start = 0
    if y_start < 0: y_start = 0
    if x_finish < 0: x_finish = 0
    if y_finish < 0: y_finish = 0

    if x_start > img_size[0]: x_start = img_size[0]
    if x_finish > img_size[0]: x_finish = img_size[0]
    if y_start > img_size[1]: y_start = img_size[1]
    if y_finish > img_size[1]: y_finish = img_size[1]

    if x_start > x_finish:
        box.append(x_finish)
        if y_start > y_finish:
            box.append(y_finish)
            box.append(x_start)
            box.append(y_start)
        else:
            box.append(y_start)
            box.append(x_start)
            box.append(y_finish)
    else:
        box.append(x_start)
        if y_start > y_finish:
            box.append(y_finish)
            box.append(x_finish)
            box.append(y_start)
        else:
            box.append(y_start)
            box.append(x_finish)
            box.append(y_finish)
    return box


def img_crop(img, where, x_start, y_start, x_finish, y_finish):
    try:
        imageFile = Image.open(img)
        box = sort_parts(x_start, y_start, x_finish, y_finish, imageFile.size)
        region = imageFile.crop(box)
        region.save(where + cropped_name + ext)
    except SystemError as e:
        print "System Error, {0}".format(e)

img_crop('res/test_pil.jpg','res/', 1, 2, 5, 5)
