import os # , sys, io
import argparse
from pathlib import Path
from PIL import Image


xfp_vmax = 225 # Do not change
xfp_hmax = 384 # Do not change
sfp_vmax = 0
sfp_hmax = 0
clamshell_vmax = 475 # Do not change
clamshell_hmax = 700 # Do not change
shipping_vmax = 0
shipping_hmax = 0

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

def resizeimage(imgv, imgh, maxv, maxh):
    '''
    Next, I want to proportionally resize the image to fit
    the max dimensions provided.
    '''
    print('Image horizontal max: ', str(img_hmax))
    print('Image vertical max: ', str(img_vmax))
    print('Image dimensions before conversion: ', str(imgh) + '*' + str(imgv))
    # determine horizontal correction factor
    hfactor = maxh / imgh
    # determine vertical correction factor
    vfactor = maxv / imgv

    # select the lowest factor to prevent oversizing the image
    factor = min(vfactor, hfactor)

    # print(factor)

    # determine new size
    newh = imgh * factor
    newv = imgv * factor

    # set and return tuple
    newsize = (newh, newv)
    return newsize


def saveimage(path, infile):
    ext = right(infile, 4)
    if ext.lower() != '.bmp':
        f, e = infile.split('.')
        outfile = path + '/' + f + '.bmp'
    else:
        outfile = path + '/' + infile
    try:
        img.save(outfile)
    except:
        print('Error converting image to bitmap')


if __name__ == '__main__':
    '''
    Parse the arguments passed into the software
    then set environment variables
    '''
    THISCODEFILEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')
    THISCODEFILE = __file__ # or sys.argv[0]
    parser = argparse.ArgumentParser(description='This software will convert the image file entered into a usable'
                                                 'format and size (proportionally) for the Label Printers.  A file'
                                                 'name is required to run.  If no path is entered, it is assumed'
                                                 'that the file is located in the same directory this script is ran from.')
    parser.add_argument('--path', type=str, help='The full path of the file.', required=False)
    parser.add_argument('--filename', type=str, help='The full file name.', required=True)
    parser.add_argument('--printer', type=int, help='1 = XFP, 2 = SFP, 3 = Clamshell, 4 = Shipping', required=True)
    args = parser.parse_args()
    if not args.path:
        path = THISCODEFILEDIR
    else:
        path = args.path

    filename = args.filename
    filetype = right(filename, 3)
    printer = args.printer
    fullpath = path + '/' + filename

    file = Path(fullpath)

    if file.is_file():
        if printer == 1:
            img_hmax = xfp_hmax
            img_vmax = xfp_vmax
        elif printer == 2:
            img_hmax = sfp_hmax
            img_vmax = sfp_vmax
        elif printer == 3:
            img_hmax = clamshell_hmax
            img_vmax = clamshell_vmax
        elif printer == 4:
            img_hmax = shipping_hmax
            img_vmax = shipping_vmax

        print('Opening: ', fullpath)

        # Open the image
        img = Image.open(fullpath).convert('1')

        # load dimensions into readable variables
        loaded_hdim = img.size[0]
        loaded_vdim = img.size[1]

        # Check that the image dimensions are within the specified limits
        if loaded_hdim >= img_hmax or loaded_hdim < img_hmax or loaded_vdim >= img_vmax or loaded_vdim < img_vmax:
            print(resizeimage(loaded_hdim, loaded_vdim, img_hmax, img_vmax)) # img.resize(resizeimage(loaded_hdim, loaded_vdim, img_hmax, img_vmax))

        # remove color from the image, greyscale.  Use '1' for pure B/W
        # img.convert('L')

        # save new image
        saveimage(path, filename)
    else:
        print('File does not exist or file name is not correct at the following location: ', fullpath)
