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