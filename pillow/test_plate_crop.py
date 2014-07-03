__author__ = 'Imressed'

import unittest
from PIL import Image
from pillow.pillow_try import img_crop, sort_parts

class TestImgCropp(unittest.TestCase):

    def setUp(self):
       self.goodsort1 = [200, 100, 600, 300]
       self.badsort1 =  [600, 300, 200, 100]
       self.x_start=100
       self.y_start=200
       self.x_finish=400
       self.y_finish=487
       self.img_size = (800,800)

    def test_sort(self):
       self.assertEqual(sort_parts(self.badsort1[0],self.badsort1[1],
                                   self.badsort1[2],self.badsort1[3],
                                   self.img_size), self.goodsort1)

    def test_negative(self):
       self.assertEqual(sort_parts(-2,-3,100,-6, self.img_size), [0,0,100,0])

    def test_extra_large(self):
       self.assertEqual(sort_parts(1000, 400, 300, 100000, self.img_size),
                                    [300, 400, 800, 800])

    def test_crop(self):
        img_crop('res/test_pil.jpg','res/', self.x_start, self.y_start,
                                            self.x_finish, self.y_finish)
        im=Image.open('res/CROPPED.jpg')
        self.assertEqual(im.size, (abs(self.x_finish - self.x_start),
                                   abs(self.y_finish - self.y_start)))


if __name__ == '__main__':
    unittest.main()