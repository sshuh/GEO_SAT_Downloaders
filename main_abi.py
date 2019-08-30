# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 17:19:18 2018

@author: sshuh
"""

# pip install awscli
# aws --version

#import datetime
from dateutil.parser import parse
import subprocess
import os
import numpy as np
import cv2
from netCDF4 import Dataset


def abi_download( _str_inputdate ):
    
    ### search inputdate in aws server

#    yearday = datetime.date.today().timetuple().tm_yday
#    print(yearday)
    
#    str_inputdate = '20180910_160000'
    str_inputdate = _str_inputdate
    
    str_inputdate_reform = str_inputdate[0:8] + str_inputdate[9:]
    
    parsed_date = parse(str_inputdate_reform)
    
    str_year = parsed_date.strftime("%Y")
    str_yday = (f'{(parsed_date.timetuple().tm_yday):03}')
    str_hour = parsed_date.strftime("%H")
    str_min = parsed_date.strftime("%M")
    
    cmd_ls = 'aws s3 --no-sign-request ls noaa-goes16/ABI-L1b-RadF/' + str_year + '/' + str_yday + '/' + str_hour + '/'
    
    #str_month = parsed_date.strftime("%m")
    #str_day = parsed_date.strftime("%d")
    


    ### read filenames at the date and make a list
    
    str_ls = str(subprocess.check_output(cmd_ls, shell=True))
    
    idx = 0
    name_begin = 0
    list_filenames = []
    
    while name_begin >= 0:
        name_begin, name_end = str_ls[idx:].find('OR_'), str_ls[idx:].find('.nc')+3
        
        if name_begin < 0 or name_end < 0:
            break
        
        list_filenames.append(str_ls[idx+name_begin:idx+name_end])
        idx = idx+name_end
       
        
    ### find files corresponding minute
    
    list_filenames_16ch = []
    str_imagingtime = 's' + str_year + str_yday + str_hour + str_min
    for filename in list_filenames:
        idx = filename.find( str_imagingtime )
        if idx == 26:
            list_filenames_16ch.append( filename )
    
    if len(list_filenames_16ch) != 16:
        print('ERROR: Cannot read 16 channels!\n')
        
    if len(list_filenames_16ch) == 0:
        print('ERROR: Cannot read any files! Check the time format!\n')


    ### download files
    
    dirname_download = 'GOES16_ABI_L1B_FD_' + str_inputdate
    os.mkdir(dirname_download)
        
    for filename in list_filenames_16ch:
        cmd_cp = 'aws s3 --no-sign-request cp s3://noaa-goes16/ABI-L1b-RadF/' + str_year + '/' + str_yday + '/' + str_hour + '/' + filename + ' ./' + dirname_download
        os.system(cmd_cp)
        print( 'Downloaded:', filename )
    
    
    ### read one ch netcdf and write one image file for 16 channels
   
    dir_name = './' + dirname_download + '/'
    dir_file_list = os.listdir(dir_name)
    dir_file_list.sort()
    
    for file_name in dir_file_list:
        i_ch = int(file_name[19:21])-1
        dataset = Dataset(dir_name+file_name, 'r')
        r = dataset.variables['Rad']
        r.set_auto_maskandscale(False)
        img_fd_src = r[:]
    
        filename_img = 'img_goes16_abi_l1b_fd_ch%02d.png' % (i_ch+1)
        dirfilename = dir_name+filename_img
        cv2.imwrite( dirfilename, np.interp(img_fd_src, (img_fd_src.min(),img_fd_src.max()), (0,255)) )
        
        print( 'Write:', filename_img )

    return



#import abi_utils

def main():
    
    print('ABI fulldisk MN:00,15,30,45  SS:00')
    print('please type UTC as: YYYYMMDD_HHMNSS')
    print('ex) 20180911_121500')
    
    input_date = input()

    print('your input date: ' + input_date)
    print('please wait until downloading and converting to image are done.')
    
#    abi_utils.abi_download( input_date )
    abi_download( input_date )
    
    print('processing done.')
    

if __name__ == "__main__":
    # execute only if run as a script
    main()



