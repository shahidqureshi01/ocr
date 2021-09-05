from config import denoise_image_config as config
from pyimagesearch.denoising.helper import blur_and_threshold
from imutils import paths
import argparse
import pickle
import random
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--testing", required=True, help="path to input dataset")
ap.add_argument("-s", "--sample", required=True, help="sample size for testing images")
args = vars(ap.parse_args())

# load the model
model = pickle.loads(open(config.MODEL_PATH, "rb").read())

image_paths = list(paths.list_images(args["testing"]))
random.shuffle(image_paths)
image_path = image_paths[:int(args["sample"])]

for image_path in image_paths:
  print('processing...{}'.format(image_path))
  image = cv2.imread(image_path)
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
  copy = image.copy()

  # adding padding 2 pixels to each side
  image = cv2.copyMakeBorder(image, 2, 2, 2, 2, cv2.BORDER_REPLICATE) 
  image = blur_and_threshold(image)

  # region feature extraction
  region_features = []

  for y in range(0, image.shape[0]):
    for x in range(0, image.shape[1]):
      # extract the region 
      region = image[y:y+5, x:x+5]
      (rH, rW) = region.shape[:2]

      # continue if region is not 5x5
      if rW != 5 or rH != 5:
        continue

      # flatten the region values
      features = region.flatten()
      region_features.append(features)


