from __future__ import division

"""
Hand Pose Detection and Tracking in Videos  
- Using OpenCV 3.3 and FFMPEG  
"""

import argparse  
import os
import subprocess
from pytube import YouTube  

from os import listdir
from os.path import isfile, join

import cv2
import time
import numpy as np  

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fps', type=int, help= 'Frames per second')  
parser.add_argument('-d', '--dpath', type=str, help='Download directory', default='./saved_videos')  
args = parser.parse_args()  

# Download videos from YouTube  
youtube_prefix = 'https://youtube.com/embed/' 
playlist = 'PLegrqXHtHobDKdZDCcao5N9fweWrNIOej'

# Demo surgery videos  
videos = [{'id': 'QRW1qV2lWcE', 'start': '00:01:00'},
          {'id': 'GT-FLlE95KU', 'start': '00:02:51'},
          {'id': 'GT-FLlE95KU', 'start': '00:16:30'},
          {'id': 'xcew3ycbG50', 'start': '00:01:37'},
          {'id': 'xcew3ycbG50', 'start': '00:01:57'},
          {'id': 'xcew3ycbG50', 'start': '00:04:09'},
          {'id': 'xcew3ycbG50', 'start': '00:04:23'},
          {'id': 'iUwBjZUs_xo', 'start': '00:01:08'},
          {'id': 'VFyJ65hEF3k', 'start': '00:01:06'},
          {'id': 'txCYSkZIrjE', 'start': '00:00:08'},
          {'id': 'txCYSkZIrjE', 'start': '00:10:37'},
          {'id': 'AGQ-PTm4-HA', 'start': '00:03:45'},
          {'id': 'OtqdK-IHp5U', 'start': '00:00:35'},
          {'id': 'OtqdK-IHp5U', 'start': '00:00:26'},
          {'id': 'OtqdK-IHp5U', 'start': '00:03:03'}]  

urls = []

for video in videos:
    url = '{}{}'.format(youtube_prefix, video['id'])  
    if url not in urls:
        urls.append(url) 
"""
# Save unprocessed videos  
for url in urls:
    try:  
        YouTube(url).streams.first().download(args.dpath)  
    except:
        print(url)  
Note: did the following in colab because couldn't get past age restriction with pytube  
for video in videos:
    vid_id = video['vid']
    vid_s = video['start']
    vid_t = video['time']
    video_mp4 = 'video_id={}_start={}_time=10s.mp4'.format(vid_id, vid_s)


    YOUTUBE_ID = vid_id
    YouTubeVideo(YOUTUBE_ID)

    !rm -rf youtube.mp4
    # download the youtube with the given ID
    !youtube-dl -f 'bestvideo[ext=mp4]' --output "youtube.%(ext)s" https://www.youtube.com/watch?v=$YOUTUBE_ID
    # download videos
    !ffmpeg -y -loglevel info -i youtube.mp4 -ss $vid_s -t $vid_t $video_mp4
"""

# Load all video mp4s  
videos = [f for f in listdir(args.dpath) if isfile(join(args.dpath, f))]
video_directories = []

for video in videos:  
    print(video)  
    video_path = '{}/{}/'.format(args.dpath, video.split('.mp4')[0])  
 
    # Process video into frames with ffmpeg
    try:  
        os.mkdir(video_path)  
    except:
        pass
    # subprocess.call(['ffmpeg', '-i', '{}/{}'.format(args.dpath, video), '-r', str(args.fps), '{}/output_%0{}d.png'.format(video_path, len(str(10 * args.fps)))])  
    video_directories.append(video_path)  

"""
Start hand tracking
"""

# Load pre-trained models and parameters   
protoFile = "hand/pose_deploy.prototxt"
weightsFile = "hand/pose_iter_102000.caffemodel"

nPoints = 22  
threshold = 0.01

POSE_PAIRS = [ [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20] ]
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)  


def model_fit(model, fname, num_points=nPoints):  
    """Extract features from frame"""  
    frame = cv2.imread(fname)  
    frame_copy = np.copy(frame)  
    frame_w = frame.shape[1]  
    frame_h = frame.shape[0]  
    aspect_ratio = frame_w / frame_h  
    
    t = time.time()
    # Input image dimensions for the network  
    inHeight = 368
    inWidth = int(((aspect_ratio*inHeight)*8)//8)
    inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False)
    
    model.setInput(inpBlob)  
    print("time taken by network : {:.3f}".format(time.time() - t))  
    return model.forward(), frame, frame_copy, frame_w, frame_h

def get_keypoints(model, frame_copy, width, height, num_points=nPoints):
    """Retrieve detected hand keypoints"""
    points = []  
    
    for i in range(num_points):
        # confidence map of corresponding body's part  
        prob_map = model[0, i, :, :]
        prob_map = cv2.resize(prob_map, (width, height))  

        # Find global maxima of probabilities  
        min_val, prob, min_loc, point = cv2.minMaxLoc(prob_map)  
        
        if prob > threshold:  
            cv2.circle(frame_copy, (int(point[0]), int(point[1])), 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)  
            cv2.putText(frame_copy, "{}".format(i), (int(point[0]), int(point[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv2.LINE_AA)  
            # Add the point to the list if the probability is greater than the threshold
            points.append((int(point[0]), int(point[1])))
        else:
            points.append(None)  
    return points  

def get_skeleton(frame, points):  
    """Get skeleton representation for detection"""  
    for pair in POSE_PAIRS:  
        part_a = pair[0]  
        part_b = pair[1]  
        
        if points[part_a] and points[part_b]:  
            cv2.line(frame, points[part_a], points[part_b], (0, 255, 255), 2)  
            cv2.circle(frame, points[part_a], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
            cv2.circle(frame, points[part_b], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)  

## Actual processing
for vdir in [video_directories[4]]:
    frames = [f for f in listdir(vdir) if isfile(join(vdir, f))]   
    # print(frames)  
    # print(vdir)  
    ix = 0
    for frame_name in frames:
        frame_path = '{}{}'.format(vdir, frame_name)  
        net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)  
        updated_net, frame1, frame_copy1, width, height = model_fit(net, frame_path)  
        points = get_keypoints(updated_net, frame_copy1, width, height)  
        get_skeleton(frame1, points)  
        print('{}/skeleton-{}.jpg'.format(vdir, ix))  
        cv2.imwrite('{}/skeleton-{}'.format(vdir, frame_name), frame1)
        cv2.imwrite('{}/keypoints-{}'.format(vdir, frame_name), frame_copy1)
        ix += 1  






