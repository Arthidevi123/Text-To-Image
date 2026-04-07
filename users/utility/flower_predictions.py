import os
import numpy as np
from keras.preprocessing import image
# from keras.models import model_from_json
from tensorflow.python.keras.models import model_from_json
from django.conf import settings


def start_prediction(flower_path):
    class_dict = {0: 'daisy', 1: 'dandelion', 2: 'rose', 3: 'sunflower', 4: 'tulip'}
    model_json = os.path.join(settings.MEDIA_ROOT, 'models', 'model.json')
    print("Json path is ", model_json)
    json_file = open(model_json, 'r')
    model_json = json_file.read()
    json_file.close()
    from tensorflow.keras.models import model_from_json
    model = model_from_json(model_json)
    model_path = os.path.join(settings.MEDIA_ROOT, 'models', 'model.h5')
    import tensorflow as tf
    #model = tf.keras.models.load_model(model)
    model.load_weights(model_path)
    print(model.summary())
    test_path = os.path.join(settings.MEDIA_ROOT, flower_path)
    flower_path = image.load_img(test_path, target_size=(240, 320, 3))
    flower_path = image.img_to_array(flower_path)
    flower_path = np.expand_dims(flower_path, axis=0)
    predicted_class = np.argmax(model.predict(flower_path), axis=1)[0]
    result = str(class_dict[predicted_class])
    print('Predicted Image Class : ' + result)
    return result, test_path

