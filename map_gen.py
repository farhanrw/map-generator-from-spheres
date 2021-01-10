import os
from tqdm import tqdm
import glob
import numpy as np
import math
from PIL import Image

all_images = sorted(glob.glob('images/*.png'), key=os.path.getmtime)
all_data = sorted(glob.glob('data/*.txt'), key=os.path.getmtime)
point_angles = []

def getPhi(x, y, z):
    value = math.degrees(math.atan2(math.sqrt(x**2+z**2), y))
    if value >= 0:
        return value 
    return (value+360)%360
def getTheta(x, y, z):
    value = math.degrees(math.atan2(z, x)) # x is the standard
    if value >= 0:
        return value 
    return (value+360)%360

def worker(x,y):
    x = int(x)
    y = int(y)
    if(x==20 and y==1):
        return 0
    if(x==20 and y==46):
        return 1
    if(x==20 and y==91):
        return 2
    if(x==20 and y==136):
        return 3
    if(x==20 and y==181):
        return 4
    if(x==20 and y==226):
        return 5
    if(x==20 and y==271):
        return 6
    if(x==20 and y==316):
        return 7
    if(x==50 and y==1):
        return 8
    if(x==50 and y==46):
        return 9
    if(x==50 and y==91):
        return 10
    if(x==50 and y==136):
        return 11
    if(x==50 and y==181):
        return 12
    if(x==50 and y==226):
        return 13
    if(x==50 and y==271):
        return 14
    if(x==50 and y==316):
        return 15
    if(x==80 and y==1):
        return 16
    if(x==80 and y==46):
        return 17
    if(x==80 and y==91):
        return 18
    if(x==80 and y==136):
        return 19
    if(x==80 and y==181):
        return 20
    if(x==80 and y==226):
        return 21
    if(x==80 and y==271):
        return 22
    if(x==80 and y==316):
        return 23

all_images = sorted(glob.glob('/home/farhan/Farhan_Thesis_Codes/pbrt_experiments/spheres-color-2/imgs/*.png'), key=os.path.getmtime)
indices = sorted(glob.glob('indices-new/*.txt'), key=os.path.getmtime)
index_data = np.zeros((24, 122483, 4), dtype='int')
for i in range(len(indices)):
    index_filename = (os.path.splitext(os.path.basename(indices[i]))[0]).split('_')
    index_of_index = worker(index_filename[3], index_filename[5])
    index_data[i] = np.loadtxt(indices[index_of_index], delimiter = ', ', dtype='int')
    
for d in tqdm(range(len(all_images))):
    
    image_filename = (os.path.splitext(os.path.basename(all_images[d]))[0]).split('_')
    sphere_image = np.asarray(Image.open(all_images[d]).convert("RGB"))
    gt_phi, gt_theta = image_filename[1], image_filename[2]
    
    cam_index = worker(gt_phi, gt_theta)
    map_image = np.zeros((60, 120, 4))
    stats = np.zeros((60, 120, 1))
    map_image[(index_data[cam_index][:,2]-1)//3, (index_data[cam_index][:,3]-1)//3, 0:3] = sphere_image[index_data[cam_index][:,1], index_data[cam_index][:,0]]
    map_image[(index_data[cam_index][:,2]-1)//3, (index_data[cam_index][:,3]-1)//3,3] = 255 
    stats[(index_data[cam_index][:,2]-1)//3, (index_data[cam_index][:,3]-1)//3] += 1
#     for i in range(len(index_data[cam_index])):
#         x_pixel, y_pixel = index_data[cam_index][i][0:2]
#         phi, theta = index_data[cam_index][i][2:4]
#         map_image[int(phi)-1, int(theta)-1] += sphere_image[int(x_pixel), int(y_pixel)]
#         stats[int(phi)-1, int(theta)-1] += 1
    map_image[:,:,0:3] = map_image[:,:,0:3]/stats
    #map_image = np.nan_to_num(map_image/stats)
    map_image = Image.fromarray(np.uint8(map_image))
    file_name = '/home/farhan/Farhan_Thesis_Codes/pbrt_experiments/spheres-color-2/maps-transparent/map_' + os.path.splitext(os.path.basename(all_images[d]))[0] + '.png'
    map_image.save(file_name)