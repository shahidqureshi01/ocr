from operator import index
from helper import OUTPUT_LAYERS
from helper import decode_predictions
from helper import cleanup_text
import numpy as np
import cv2
import time
import pytesseract
import pandas as pd
from imutils.contours import sort_contours

model = 'read_image/models/frozen_east_text_detection.pb'
height = 640*2
width = 640*2
conf_score = 0.5
thresh = 0.4
padding = 0.0
sort = 'top-to-bottom'
results = []

def detect(img_path):
  img = cv2.imread(img_path)

  (original_height, original_width) = img.shape[:2]

  rW = original_width /float(width)
  rH = original_height /float(height)

  print('loading EAST....')

  net = cv2.dnn.readNet(model)
  blob = cv2.dnn.blobFromImage(img, 1.0, (height, width), (123.68, 116.78, 103.94), swapRB=True, crop=False)
  start = time.time()
  net.setInput(blob)
  (scores, geometry) = net.forward(OUTPUT_LAYERS)

  end = time.time()

  print('EAST took {:.6f} seconds'.format(end - start))

  # decode the predictions, then  apply non-maxima suppression to suppress weak, overlapping bounding boxes
  (rect, confidences) = decode_predictions(scores, geometry)
  #print('confidences is {}'.format(confidences))

  idx = cv2.dnn.NMSBoxesRotated(rect, confidences, conf_score, thresh)

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
      #cv2.polylines(img, [box], True, (0,255,0), 3)
      # convert rotated box to normal box
      (x, y, w, h) = cv2.boundingRect(box)
      # compute the deltas for padding
      dX = int((w * padding))
      dY = int((h * padding))

      # apply padding to each side of the bounding box, respectively
      start_X = max(0, x - dX)
      start_y = max(0, y - dY)
      end_x = min(original_width, x + w + (dX * 2))
      end_y = min(original_height, y + h + (dY * 2))
      padded_region = img[start_y:end_y, start_X:end_x]

      # apply OCR to the padded region
      options = '--psm 7'
      text = pytesseract.image_to_string(padded_region, config=options)
      results.append((box, text))
  return sorted(results, key=lambda r:r[0][0][1])
	




