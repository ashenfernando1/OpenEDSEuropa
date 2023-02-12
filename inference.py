import tensorflow as tf
import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import time
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("vid")
args = parser.parse_args()

model = tf.keras.models.load_model('model')

def model_use(input_frame):
    frame = input_frame.copy()
    frame = frame[-240:,:,:]
    frame = cv2.resize(frame, (128,128))
    frame = frame.astype(np.float32) / 255.0
    
    mask = model.predict(np.expand_dims(frame, axis=0), verbose=0)
    pred_mask = tf.math.argmax(mask, axis=-1)
    pred_mask = pred_mask[..., tf.newaxis]
  
    return pred_mask[0]


start = time.time()
# Open the video file
vid = args.vid
print(vid)
input_video = cv2.VideoCapture(vid)

# Get the video dimensions and frames per second
# width = 240
# height = 240
# fps = int(input_video.get(cv2.CAP_PROP_FPS))

# Define the codec and create the video writer object
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# output_video = cv2.VideoWriter("trim_pred.mp4", fourcc, fps, (width, height), False)
area_counts = []
# Loop through the frames of the input video
while True:
    success, frame = input_video.read()
    if not success:
        break
    
    # Modify the frame here (e.g. add a filter, resize, etc.)
    predicted_frame = model_use(frame).numpy().astype(dtype=np.uint8)
    # plt.imshow(predicted_frame)
    frame_counts = list(np.unique(predicted_frame, return_counts=True))
    # Write the modified frame to the output video
    # output_video.write(predicted_frame)
    area_counts.append(frame_counts)

# Release the video capture and writer objects
input_video.release()
# output_video.release()

print(f'Time for script: {(time.time() - start):.2f}')

areas_pd = pd.DataFrame([i[1] for i in area_counts], columns = ['bg', 'sclera', 'iris', 'pupil'])
areas_pd['total'] = areas_pd[['sclera','iris','pupil']].sum(axis=1)
areas_pd['sclera'] = areas_pd['sclera']/areas_pd['total']
areas_pd['iris'] = areas_pd['iris']/areas_pd['total']
areas_pd['pupil'] = areas_pd['pupil']/areas_pd['total']

areas_pd.to_csv('outputs/' + '_'.join(vid.split('.')[0].split('/')[-1].split('_')[1:]) + '/' + vid.split('/')[-1].split('.')[0] + '.csv')

#ax = areas_pd[['sclera','iris','pupil']].plot(figsize=(12,4), title='Ratios of eye regions', )
#ax.set_xticklabels([i/50 for i in ax.get_xticks()])
#plt.savefig('ratios.png')
