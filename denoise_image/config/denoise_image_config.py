import os

cwdir = os.getcwd()

BASE_PATH = 'denoise_image/dirty-documents'

TRAIN_PATH = os.path.sep.join([BASE_PATH, 'train'])

CLEANED_PATH = os.path.sep.join([BASE_PATH, 'train_cleaned'])

FEATURES_PATH = 'features.csv'

SAMPLE_PROB = 0.02

MODEL_PATH = 'model.pkl'