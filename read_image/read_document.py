from helper import OUTPUT_LAYERS
from helper import decode_predictions
import numpy as np
import cv2

img_path = ''
model = ''
height = 0
width = 0
conf_score = 0
thresh = 0.5

img = cv2.imread(img_path)
(original_height, original_width) = img.shape[:2]

