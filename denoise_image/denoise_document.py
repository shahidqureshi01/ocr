from config import denoise_image_config as config
from pyimagesearch.denoising.helper import blur_and_threshold
from imutils import paths
import argparse
import pickle
import random
import cv2