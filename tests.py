import unittest
from utils import photo_sizer, map_sizer

class TestPhotoSizer(unittest.TestCase):

    def setUp(self):
        self.photo_sizes1 = photo_sizer(1055, 1000, '###')
        self.photo_sizes2 = photo_sizer(1000,  1095, '###')
        self.photo_sizes3 = photo_sizer(1000,  1200, '###')
        self.photo_sizes4 = photo_sizer(1000,  1333, '###')
        self.photo_sizes5 = photo_sizer(1000, 1400, '###')
        self.photo_sizes6 = photo_sizer(1000,  1600, '###')
        self.photo_size7 = photo_sizer(1000,  1800, '###')
        self.photo_size8 = photo_sizer(1000,  1900, '###')
        self.photo_size9 = photo_sizer(1000,  2000, '###')
        self.photo_size10 = photo_sizer(1000,  2000, '###')
        self.photo_size11 = photo_sizer(1000,  2200, '###')
        self.photo_size12 = photo_sizer(1000,  2500, '###')
        self.photo_size13 = photo_sizer(1000,  2700, '###')
        self.photo_size14 = photo_sizer(1000,  2900, '###')
        self.photo_size15 = photo_sizer(1000,  3100, '###')
        self.photo_size16 = photo_sizer(1000,  1000, '###')

    def test_sizenames(self):
        list1 = ['12in x 12in', '16in x 16in', '24in x 24in', '36in x 36in', '44in x 44in']
        assertion = True if False not in [size['SizeName'] in list1 for size in self.photo_sizes1 ] else False
        self.assertTrue(assertion)
    '''
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    '''

if __name__ == '__main__':
    unittest.main()