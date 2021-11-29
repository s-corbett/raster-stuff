# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 16:23:48 2021

@author: Test
"""

import rasterio as rio
import numpy as np
import itertools

wind_path = "D:/Global Bathy Wind/clipped/clipped/wind_extract_s.tif"
# wind_path = 'D:/Global Bathy Wind/GWA_windspeed_100m/reclassed/reclass_100.tif'

bathy_path = "D:/Global Bathy Wind/clipped/clipped/bathy_extract_s.tif"
# bathy_path = 'D:/Global Bathy Wind/GEBCO_grid/reclass_50_1000_v2/mosaic/rGebco_50_1000_mosaic.tif'



# open reclassed windspeed file
with rio.open(wind_path) as wsrc:
    
    # name outfile
    out_file = 'D:/Global Bathy Wind/clipped/clipped/output/output_file_breakdown.tif'
    
    # copy profile
    out_profile = wsrc.profile.copy()
    
    # make outfile
    dst = rio.open(out_file, 'w', **out_profile)
    
    # open reclassed bathymetry file
    with rio.open(bathy_path) as bsrc:
    
        # create blocks in windspeed
        for block_index, window in wsrc.block_windows(1):
            
            print('READING NEW BLOCK')
            
            # read first band of block in windspeed file
            block_array = wsrc.read(1, window=window)
            
            # # print shape of block
            print('Block array shape: ', block_array.shape[0], block_array.shape[1])
            
            # # create empty array with length matching block array
            # new_array = np.empty(block_array.shape[1])
            new_array = np.empty(block_array.shape)
            
            # set current index to 0
            cur_idx = 0
            
            # set current array to pos 0
            arr = 0
            
            for row, col in itertools.product(range(block_array.shape[0]), range(block_array.shape[1])):
                
                # print(row, col)
                
                # get value at position in original block
                val = block_array[(row, col)]
                
                # this block below would check that we are distinguishing between 1 and 0 in the other file correctly
                # if next(bsrc.sample([wsrc.xy(row, col)]))[0] == 1:
                    
                #     print('SAMPLE IS 1: ', next(bsrc.sample([wsrc.xy(row, col)]))[0])
                    
                # else:
                    
                #     print('Sample is other: ', next(bsrc.sample([wsrc.xy(row, col)]))[0])
                
                #print('SAMPLE: ', next(bsrc.sample([wsrc.xy(row, col)]))[0])
                
                # if value is 1, get value in other file
                if val == 1 and next(bsrc.sample([wsrc.xy(row, col)]))[0] == 1:
                    
                    # print("Value in both files is 1: ", val, ', ', next(bsrc.sample([wsrc.xy(row, col)]))[0])
                    
                    # populate output array with correct value 2
                    new_array[arr][col] = 2
                    
                else:
                    
                    print("Value in both files is not 1: ", val, ', ', next(bsrc.sample([wsrc.xy(row, col)]))[0])
                    
                    # populate output array with correct value NaN
                    new_array[arr][col] = np.nan
                    
            
            # check if 2 is in the array here
            if 2 in new_array:
                
                print("*** New values found in output")
        
            # reshape the array to match rasterio format - (band, row, col)
            # new_array = new_array.reshape((1, block_array.shape[0], block_array.shape[1]))
            new_array = new_array.reshape((1, new_array.shape[0], new_array.shape[1]))    
        
            # write the block 
            dst.write(new_array, window=window)
                    
            
        wsrc.close()
        bsrc.close()
        dst.close()
        

