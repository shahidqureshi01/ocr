from helper import OUTPUT_LAYERS
from helper import decode_predictions
import numpy as np
import cv2
import time

img_path = ''
model = ''
height = 0
width = 0
conf_score = 0
thresh = 0.5

img = cv2.imread(img_path)
(original_height, original_width) = img.shape[:2]

rW = original_width /float(width)
rH = original_height /float(height)

print('loading EAST....')

net = cv2.dnn.readNet('EAST')

blob = cv2.dnn.blobFromImage(img, 1.0, (width, height), (123.68, 116.78, 103.94), swapRB=True, crop=False)
start = time.time()
net.setInput(blob)
(scores, geometry) = net.forward(OUTPUT_LAYERS)
end = time.time()

print('EAST took {:.6f} seconds'.format(end - start))

# decode the predictions, then  apply non-maxima suppression to suppress weak, overlapping bounding boxes
(rect, confidences) = decode_predictions(scores, geometry)
idx = cv2.dnn.NMSBoxes(rect, confidences, conf_score, thresh)

if len(idx) > 0:
    # loop over the indexes we are keeping
    for i in idx.flatten():
        # extract the bounding box coordinates
        box = cv2.boxPoints(rect[i])
        # scale the bounding box coordinates based on the respective ratios
        box[:,0] = box[:,0] * rW
        box[:,1] = box[:,1] * rH
        box= np.int0(box)

        # draw the bounding box on the image
        cv2.polylines(img, [box], True, (0,255,0), 3)

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows(1)