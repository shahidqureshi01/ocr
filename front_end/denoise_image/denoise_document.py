# from denoise_image.config import *
from denoise_image.config import denoise_image_config as config
from denoise_image.pyimagesearch.denoising.helper import blur_and_threshold
from imutils import paths
import pickle
import cv2

# load the model
model = pickle.loads(open(config.MODEL_PATH, "rb").read())

img_path = 'denoise_image/dirty-documents/test/61.png'
def denoise(img_path):
  img = cv2.imread(img_path)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
  copy = img.copy()

  # add padding 
  img = cv2.copyMakeBorder(img, 2, 2, 2, 2, cv2.BORDER_REPLICATE) 
  img = blur_and_threshold(img)

  region_features = []

  for y in range(0, img.shape[0]):
    for x in range(0, img.shape[1]):
      # extract the region 
      region = img[y:y+5, x:x+5]
      (rH, rW) = region.shape[:2]

      # continue if region is not 5x5
      if rW != 5 or rH != 5:
        continue

      # flatten the region values
      features = region.flatten()
      region_features.append(features)

  # predict the image
  pixels = model.predict(region_features)

  # reshape the image as per original image size
  pixels = pixels.reshape(copy.shape)
  # change values between 0 and 255
  output = (pixels * 255).astype("uint8")
  return output
# cv2.imshow('original', copy)
# cv2.waitKey(0)
# cv2.imshow('clean', output)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imwrite('61.png', output)


