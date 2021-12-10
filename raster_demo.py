# This is some demo code I received from my old lecturer at university
# this works for a test tif, but line 23 doesn't work for the accessing 
# the image coords of the x, y points in the second (bathymetry) dataset
# because that code is trying to load a whole file into memory,
# and the bathymetry file I need to use is too large to do that with.

from rasterio import open as rio_open

# load raster
with rio_open("test.tif") as input:

    # get first band
    band1 = input.read(1)

    # loop through raster
    for row in range(band1.shape[0]):
        for col in range(band1.shape[1]):

            # get coords in geographical space
            x, y = input.xy(row, col)
            
            # get coordinates in image space (again...)
            r, c = input.index(x, y)

            # get value at that location
            v = band1[(r, c)]

            # print all of that out
            print(row, col, x, y, r, c, v)
