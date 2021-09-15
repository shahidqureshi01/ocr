import numpy as np
#OUTPUT_LAYERS = ['feature_fusion/conv_7/sigmoid', 'feature_fusion/concat_3']
OUTPUT_LAYERS = ["feature_fusion/Conv_7/Sigmoid","feature_fusion/concat_3"]

def cleanup_text(text):
  return "".join([c if ord(c) < 128 else "" for c in text]).strip()

def decode_predictions(scores, geometry, min_score=0.5):
  # grab row and columns  from scores
  num_rows = scores.shape[2]
  num_cols = scores.shape[3]

  rects = []
  confidences = []

  # loop over the number of rows
  for y in range(0, num_rows):
    # extract the scores (probabilities), followed by the
    # geometrical data used to derive potential bounding box
    # coordinates that surround text
    scores_data = scores[0, 0, y]
    x0_data = geometry[0, 0, y]
    x1_data = geometry[0, 1, y]
    x2_data = geometry[0, 2, y]
    x3_data = geometry[0, 3, y]
    angles_data = geometry[0, 4, y]

    # loop over the number of columns
    for x in range(0, num_cols):
      score = float(scores_data[x])
      # if our score does not have sufficient probability,
      # ignore it
      if score < min_score:
        continue

      # compute the offset factor as our resulting feature
      # maps will be 4x smaller than the input image
      (offset_x, offset_y) = (x * 4.0, y * 4.0)

      # extract the rotation angle for the prediction and
      # then compute the sin and cosine
      angle = angles_data[x]
      cos = np.cos(angle)
      sin = np.sin(angle)

      # use the geometry volume to derive the width and height
      # of the bounding box
      h = x0_data[x] + x2_data[x]
      w = x1_data[x] + x3_data[x]

      # compute both the starting and ending (x, y)-coordinates
      # for the text prediction bounding box
      offset = (int(offset_x + (cos * x1_data[x]) + (sin * x2_data[x])), int(offset_y - (sin * x1_data[x]) + (cos * x2_data[x])))

      top_left = ((-sin * h) + offset[0], (-cos * h) + offset[1])
      bottom_right = ((-cos * w) + offset[0], (sin * w) + offset[1])

      c_x = 0.5 * (top_left[0] + bottom_right[0])
      c_y = 0.5 * (top_left[1] + bottom_right[1])

      box = ((c_x, c_y), (w, h), -1 * angle * 180.0 / np.pi)

      rects.append(box)
      confidences.append(score)
  return (rects, confidences)