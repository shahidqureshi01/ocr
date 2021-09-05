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