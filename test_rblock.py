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
    out_file = 'D:/Global Bathy Wind/clipped/clipped/output/output_file.tif'
    
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
            
        
            # list comprehension to return values in the array
            for idx, val in enumerate([ 2 if block_array[(row, col)] == 1 and next(bsrc.sample([wsrc.xy(row, col)]))[0] == 1 else np.nan for row, col in itertools.product(range(block_array.shape[0]), range(block_array.shape[1])) ]):
                
                # index can range between 0 and block_array.shape[1] ?
                # when index < block_array.shape[1] is not true
                # add 1 to the arr variable?
                
                # print('INDEX: ', idx)
                # print('VALUE: ', val)
                
                # arr refers to which number array is being looked at
                # e.g. here the shape is 1, 1276 for most windows, but if it was 256, 256
                # then that would be 256 arrays that each have 256 positions
                # new_array[0][idx] = val
                new_array[arr][idx] = val
                
                
                # update the current index value
                cur_idx = cur_idx + 1
                
                # check if current index is less than max, otherwise arr + 1
                # if cur_idx < block_array.shape[1]:
                    
                #     # new_array[arr][idx] = val
                #     new_array[0][idx] = val
                
                # else:
                    
                #     print('cur_idx is not less than ', block_array.shape[1], ' -- cur_idx = ', cur_idx)
                #     arr = arr + 1
            
                
            print("Max index value: ", cur_idx)
                
            # check if 2 is in the array
            # if 2 in new_array:
            #     print("New value written")    
    
            
            # reshape the array to match rasterio format - (band, row, col)
            # new_array = new_array.reshape((1, block_array.shape[0], block_array.shape[1]))
            new_array = new_array.reshape((1, new_array.shape[0], new_array.shape[1]))
            
            #get shape of new array
            #print('Writing array with shape: ', new_array.shape)
            
            # check if 2 is in the array here
            if 2 in new_array:
                
                print("New values found in output")
        
            
            # write the block 
            dst.write(new_array, window=window)
            # indexes=1
            
        wsrc.close()
        bsrc.close()
        dst.close()
        

