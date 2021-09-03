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

  # padding 2px each side for both train and clean images
  train_image = cv2.copyMakerBorder(train_image, 2, 2, 2, 2, cv2.BORDER_REPLICATE)
  clean_image = cv2.copyMakerBorder(train_image, 2, 2, 2, 2, cv2.BORDER_REPLICATE)

  # blur the train image
  train_image = blur_and_threshold(train_image)

  # scale to px intensity to 0-1 from 0-255
  clean_image = clean_image.astype('float') / 255.0

  # 5x5 sliding window throgh images
  for y in range(0, train_image.shape[0]):
    for x in range(0, train_image.shape[1]):
      # extract the region for both clean and train image
      train_region = train_image[y:y + 5, x:x + 5]
      clean_region = clean_image[y:y + 5, x:x + 5]
      (rH, rW) = train_region.shape[:2]

      # discard region which is not 5x5
      if rW != 5 or rH != 5:
        continue

      # get features and target
      features = train_region.flatten()
      target = clean_region[2, 2]

      # only write a some feature/target combination to disk
      if random.random() <= config.SAMPLE_PROB:
        features = [str(x) for x in features]
        row = [str(target)] + features
        row = ', '.join(row)
        csv.write('{}\n'.format(row))
  pbar.update(i)  

# housekeeping
pbar.finish()
csv.close()

