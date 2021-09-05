from config import denoise_image_config as config 
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split  
import numpy as np
import pickle
import sys

print('loading dataset...')

features = []
targets = []

for row in open(config.FEATURES_PATH):
    # split in array and convert to float
    row = row.strip().split(',')
    row = [float(x) for x in row]
    
    # extract features and target
    f = row[1:]
    t = row[0]

    features.append(f)
    targets.append(t)
    
print(len(features))
# convert to numpy array
features = np.array(features)
targets = np.array(targets)

# split data into train and test sets
features_train, features_test, targets_train, targets_test = train_test_split(features, targets, test_size=0.2, train_size=0.8, random_state= 42)

# tranin model
print('training model...')
model = RandomForestRegressor(n_estimators=100, random_state=44)
model.fit(features_train, targets_train)

# evaulate model
pred = model.predict(features_test)
mse = np.sqrt(mean_squared_error(pred, targets_test))
print('mse: {}'.format(mse))

# save model
f = open(config.MODEL_PATH, 'wb') 
f.write(pickle.dumps(model))
f.close()

print(len(targets))



