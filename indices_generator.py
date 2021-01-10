import os
from tqdm import tqdm
import glob
import numpy as np
import math

all_images = sorted(glob.glob('images/*.png'), key=os.path.getmtime)
all_data = sorted(glob.glob('data-new/*.txt'), key=os.path.getmtime)
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

for d in tqdm(range(len(all_data))):
    face_file = np.loadtxt(all_data[d], delimiter=', ')
    pixels = face_file[:,0:2]
    point_data = face_file[:, 4:7]
    point_angles = [[int(round(pixels[i, 0])), int(round(pixels[i, 1])), int(round(getPhi(point_data[i][0], point_data[i][1], point_data[i][2]))), int(round(getTheta(point_data[i][0], point_data[i][1], point_data[i][2])))] for i in range(len(point_data))]
    np.savetxt('indices_' + os.path.basename(all_data[d]), point_angles, delimiter =', ', fmt = '%d' )