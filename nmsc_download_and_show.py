# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 14:22:43 2019

@author: sshuh
"""

import os
from PIL import Image 
from io import BytesIO 
import numpy as np
import matplotlib.pyplot as plt
import requests
import time
from datetime import datetime
from datetime import timedelta
import cv2

#%%

def nmsc_download( _str_scene, _str_time ):
    
    #_str_scene = 'KO'
    #_str_time = str_L1B_time
    str_yearmonth = _str_time[:6]
    str_day = _str_time[6:8]
    str_hour = _str_time[8:10]
    
    #url = "http://nmsc.kma.go.kr/IMG/GK2A/AMI/PRIMARY/L1B/COMPLETE/KO/201908/27/04/gk2a_ami_le1b_rgb-true_ko020lc_201908270410.png"
    url = 'http://nmsc.kma.go.kr/IMG/GK2A/AMI/PRIMARY/L1B/COMPLETE/'
    url = url + _str_scene + '/' + str_yearmonth + '/' + str_day + '/' + str_hour + '/gk2a_ami_le1b_rgb-true_' + _str_scene.lower() + '020lc_' + _str_time + '.png'

    response = requests.get(url)
    #print("binary file sample: {}".format(response.content[:20]))
    print('response.ok =', response.ok )
    
    if response.ok == True:
        
        str_png_file = (url.split('/'))[-1]
        with open(str_png_file, 'wb') as f:
            f.write(response.content)
            print(str_png_file)
            
            #img = Image.open(BytesIO(response.content))
            #img_matrix = np.array(img)
            #plt.imshow(img_matrix)
            #img.save('fff.png')
    
    return

#%%

def getDirFileList( _target_dir_name ):
    
    list_fulldir_names = []
    list_fullfile_names = []
    list_file_names = []

    list_dirs_files = os.listdir(_target_dir_name)
    for i_name in list_dirs_files:
        full_name = _target_dir_name + '/' + i_name
        if os.path.isfile(full_name):
            list_fullfile_names.append(full_name)
            list_file_names.append(i_name)
        else:
            list_fulldir_names.append(full_name)

    return list_fulldir_names, list_fullfile_names, list_file_names

#%%
    
def showLatestImage( _str_scene, _str_dir_name ):
    
    #_str_scene = 'KO'
    #_str_dir_name = 'D:/Python/nmsc_download_and_show'
    
    _, list_fullfile_names, _ = getDirFileList( _str_dir_name )
    
    list_image_names = []
    for i_name in list_fullfile_names:
        
        if (i_name.find('.png') >= 0) and (i_name.find('gk2a_ami_le1b') >= 0) and (i_name.find(_str_scene.lower()) >= 0):
            list_image_names.append( i_name )
    
    list_image_names.sort()
    
#    im = Image.open(list_image_names[-1])
#    print( im.format, im.size, im.mode )
#    im.show()
    
    img_read = cv2.imread( list_image_names[-1] )
    
    cv2.imshow('L1B', img_read )
    
    cv2.waitKey(1)
    
    return

#%%

def main():
    
#    print('ABI fulldisk MN:00,15,30,45  SS:00')
#    print('please type UTC as: YYYYMMDD_HHMNSS')
#    print('ex) 20180911_121500')
#    
#    input_date = input()
#
#    print('your input date: ' + input_date)
#    print('please wait until downloading and converting to image are done.')
    
    min_operate = 9
    str_image_dir_name = 'D:/Python/nmsc_download_and_show'
    showLatestImage( 'KO', str_image_dir_name )
    
    while 1:
        
        time_now = datetime.now()
        print(time_now)
        
        if np.mod(time_now.minute, 10) != min_operate:
            #time.sleep(58)
            cv2.waitKey(58000)
            continue
        
        
        time_L1B = time_now - timedelta(hours=9) - timedelta(minutes=10)
        str_L1B_time = time_L1B.strftime('%Y%m%d%H%M')
        str_L1B_time = str_L1B_time[:-1] + '0'
    
        
        
        
    #    abi_utils.abi_download( input_date )
        nmsc_download( 'KO', str_L1B_time )
        
        showLatestImage( 'KO', str_image_dir_name )
    
        #time.sleep(58)
        cv2.waitKey(58000)
        
#    print('processing done.')
    
#%%
        
if __name__ == "__main__":
    # execute only if run as a script
    main()



