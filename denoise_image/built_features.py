from config import denoise_image_config as config
from pyimagesearch.denoising.helper import blur_and_threshold
from imutils import paths
import progressbar
import cv2
import random


train_paths = sorted(list(paths.list_images(config.TRAIN_PATH)))
cleaned_paths = sorted(list(paths.list_images(config.CLEANED_PATH)))

widgets  = ["Creating Features: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(maxval=len(train_paths), widgets=widgets).start()

image_paths = zip(train_paths, cleaned_paths)
csv = open(config.FEATURES_PATH, 'w')

for(i, train_paths, cleaned_paths) in enumerate(image_paths):
  # read images
  train_image = cv2.imread(train_paths)
  clean_image = cv2.imread(cleaned_paths)

  #brg to gray
  train_image = cv2.cvtColor(train_image, cv2.COLOR_BGR2GRAY)
  clean_image = cv2.cvtColor(clean_image, cv2.COLOR_BGR2GRAY)
