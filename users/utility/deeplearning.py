import os

import tensorflow as tf
from django.conf import settings
from keras.models import load_model

# global graph, model, output_list
model_path = os.path.join(settings.MEDIA_ROOT, 'alexmodel', 'PlantLeavesModel.hdf5')
graph = tf.get_default_graph()
# model = load_model('./PlantDiseaseModel.hdf5')
model = load_model(model_path)
output_dict = {'Apple': 0,
               'Apple': 1,
               'Apple': 2,
               'Apple': 3,
               'Blueberry': 4,
               'Cherry': 5,
               'Cherry': 6,
               'Corn': 7,
               'Corn': 8,
               'Corn': 9,
               'Corn': 10,
               'Grape': 11,
               'Grape': 12,
               'Grape': 13,
               'Grape': 14,
               'Orange': 15,
               'Peach': 16,
               'Peach': 17,
               'Pepper': 18,
               'Pepper': 19,
               'Potato': 20,
               'Potato': 21,
               'Potato': 22,
               'Raspberry': 23,
               'Soybean': 24,
               'Squash': 25,
               'Strawberry': 26,
               'Strawberry': 27,
               'Tomato': 28,
               'Tomato': 29,
               'Tomato': 30,
               'Tomato': 31,
               'Tomato': 32,
               'Tomato': 33,
               'Tomato': 34,
               'Tomato': 35,
               'Tomato': 36,
               'Tomato': 37}

output_list = list(output_dict.keys())
