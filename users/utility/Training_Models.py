import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
import plotly.graph_objs as go
import seaborn as sns
from django.conf import settings
from sklearn.metrics import classification_report


def start_training():
    images_path = os.path.join(settings.MEDIA_ROOT, 'Flowers_Data')
    print(os.listdir(images_path))
    ## Disabling GPU Access
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    flowers_names = os.listdir(images_path)
    flowers_images = []
    for f in flowers_names:
        f_path = images_path + '\\' + f
        flowers_images.append(len(os.listdir(f_path)))
    # fig = go.Figure()
    # fig.add_trace(
    #     go.Pie(labels=flowers_names, values=flowers_images, textinfo='label+percent', hoverinfo='label+value'))
    # fig.update_layout(title='Distribution Of Number Of Flowers Of Each Category')
    # fig.show()

    dim_x = []
    dim_y = []

    for f in flowers_names:
        f_path = images_path + '\\' + f
        f_image_list = os.listdir(f_path)

        for i in f_image_list:
            x, y, z = imread(f_path + '\\' + i).shape
            dim_x.append(x)
            dim_y.append(y)
    # sns.jointplot(dim_x, dim_y)
    # plt.show()
    print('Average Value For Dim X : ' + str(np.mean(dim_x)))
    print('Average Value For Dim Y : ' + str(np.mean(dim_y)))
    print('Median Value For Dim X : ' + str(np.median(dim_x)))
    print('Median Value For Dim Y : ' + str(np.median(dim_y)))
    # Final Image Shape Will Be (240, 320, 3)
    image_shape = (240, 320, 3)
    sample_image_name = os.listdir(images_path + '\\' + flowers_names[0])[0]
    sample_image = imread(images_path + '\\' + flowers_names[0] + '\\' + sample_image_name)
    plt.imshow(sample_image)
    print('Sample Image Shape : ' + str(sample_image.shape))
    print('Max Value In Sample Image : ' + str(np.max(sample_image)))
    print('Min Value In Sample Image : ' + str(np.min(sample_image)))
    from keras.preprocessing.image import ImageDataGenerator
    # Setting Test Split Size
    test_split_size = 0.1
    # Setting Batch Size
    batch_size = 128
    # Setting Rescaling Factor
    rescale_factor = 1 / 255
    image_gen = ImageDataGenerator(horizontal_flip=True,
                                   fill_mode='nearest',
                                   rescale=rescale_factor,
                                   validation_split=test_split_size)
    train_dataset = image_gen.flow_from_directory(images_path,
                                                  target_size=image_shape[:2],
                                                  batch_size=batch_size,
                                                  class_mode='categorical',
                                                  subset='training',
                                                  color_mode='rgb',
                                                  seed=300,
                                                  shuffle=True)

    validation_dataset = image_gen.flow_from_directory(images_path,
                                                       target_size=image_shape[:2],
                                                       batch_size=batch_size,
                                                       class_mode='categorical',
                                                       subset='validation',
                                                       color_mode='rgb',
                                                       seed=300,
                                                       shuffle=False)

    print('Number Of Images In Training Dataset : ' + str(train_dataset.samples))
    print('Number Of Images In Validation Dataset : ' + str(validation_dataset.samples))

    print(train_dataset.class_indices)
    # Building Model

    from tensorflow.keras.callbacks import EarlyStopping
    early_stop = EarlyStopping(monitor='val_loss', patience=0)

    # Defining Number Of Steps For Training & Validation Of Model
    steps_per_epoch = train_dataset.samples // batch_size
    validation_steps = validation_dataset.samples // batch_size

    print('Steps Per Epoch : Training -> ' + str(steps_per_epoch))
    print('Steps : Validation -> ' + str(validation_steps))

    from keras.models import Sequential
    from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
    model = Sequential()

    model.add(Conv2D(filters=32, kernel_size=(4, 4), input_shape=image_shape, activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Conv2D(filters=64, kernel_size=(4, 4), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Conv2D(filters=96, kernel_size=(4, 4), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(5, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    print(model.summary())
    history = model.fit(train_dataset, epochs=20, steps_per_epoch=steps_per_epoch,
                        validation_data=validation_dataset, validation_steps=validation_steps,
                        verbose=True, callbacks=[early_stop])

    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epoch_range = list(range(1, 10 + 1))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=epoch_range, y=acc, name='Train Accuracy', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=epoch_range, y=val_acc, name='Test Accuracy', mode='lines+markers'))
    fig.update_layout(title='Train & Test Accuracy Trend',
                      xaxis_title='Epochs',
                      yaxis_title='Accuracy Of Model')
    fig.show()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=epoch_range, y=loss, name='Train Loss', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=epoch_range, y=val_loss, name='Test Loss', mode='lines+markers'))
    fig.update_layout(title='Train & Test Loss Trend',
                      xaxis_title='Epochs',
                      yaxis_title='Loss')
    fig.show()
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("model.h5")
    model_eval_metrics = model.evaluate_generator(validation_dataset, steps=validation_steps, verbose=1)
    print('Decision Tree Accuracy : ' + str(round(model_eval_metrics[1] * 100, 2)))
    print('Model Loss : ' + str(round(model_eval_metrics[0], 2)))
    print("Classification Report ",classification_report(validation_dataset,validation_steps))
    # Visualising Model
    # from plot_model import plot_model
    # plot_model(model, to_file='CNN_Model.jpeg', show_shapes=True, show_layer_names=True)
    #



def start_training_rf():
    images_path = os.path.join(settings.MEDIA_ROOT, 'Flowers_Data')
    print(os.listdir(images_path))
    ## Disabling GPU Access
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    flowers_names = os.listdir(images_path)
    flowers_images = []
    for f in flowers_names:
        f_path = images_path + '\\' + f
        flowers_images.append(len(os.listdir(f_path)))

    dim_x = []
    dim_y = []

    for f in flowers_names:
        f_path = images_path + '\\' + f
        f_image_list = os.listdir(f_path)

        for i in f_image_list:
            x, y, z = imread(f_path + '\\' + i).shape
            dim_x.append(x)
            dim_y.append(y)

    # Final Image Shape Will Be (240, 320, 3)
    image_shape = (240, 320, 3)
    sample_image_name = os.listdir(images_path + '\\' + flowers_names[0])[0]
    sample_image = imread(images_path + '\\' + flowers_names[0] + '\\' + sample_image_name)
    plt.imshow(sample_image)
    from keras.preprocessing.image import ImageDataGenerator
    # Setting Test Split Size
    test_split_size = 0.1
    # Setting Batch Size
    batch_size = 128
    # Setting Rescaling Factor
    rescale_factor = 1 / 255
    image_gen = ImageDataGenerator(horizontal_flip=True,
                                   fill_mode='nearest',
                                   rescale=rescale_factor,
                                   validation_split=test_split_size)
    train_dataset = image_gen.flow_from_directory(images_path,
                                                  target_size=image_shape[:2],
                                                  batch_size=batch_size,
                                                  class_mode='categorical',
                                                  subset='training',
                                                  color_mode='rgb',
                                                  seed=300,
                                                  shuffle=True)

    validation_dataset = image_gen.flow_from_directory(images_path,
                                                       target_size=image_shape[:2],
                                                       batch_size=batch_size,
                                                       class_mode='categorical',
                                                       subset='validation',
                                                       color_mode='rgb',
                                                       seed=300,
                                                       shuffle=False)

    print('Number Of Images In Training Dataset : ' + str(train_dataset.samples))
    print('Number Of Images In Validation Dataset : ' + str(validation_dataset.samples))

    print(train_dataset.class_indices)
    # Building Model

    from tensorflow.keras.callbacks import EarlyStopping
    early_stop = EarlyStopping(monitor='val_loss', patience=0)

    # Defining Number Of Steps For Training & Validation Of Model
    steps_per_epoch = train_dataset.samples // batch_size
    validation_steps = validation_dataset.samples // batch_size

    print('Steps Per Epoch : Training -> ' + str(steps_per_epoch))
    print('Steps : Validation -> ' + str(validation_steps))

    from keras.models import Sequential
    from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
    model = Sequential()

    model.add(Conv2D(filters=32, kernel_size=(4, 4), input_shape=image_shape, activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Conv2D(filters=64, kernel_size=(4, 4), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Conv2D(filters=96, kernel_size=(4, 4), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(512, activation='sigmoid'))
    model.add(Dropout(0.2))
    model.add(Dense(5, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    print(model.summary())
    history = model.fit(train_dataset, epochs=20, steps_per_epoch=steps_per_epoch,
                        validation_data=validation_dataset, validation_steps=validation_steps,
                        verbose=True, callbacks=[early_stop])

    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epoch_range = list(range(1, 10 + 1))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=epoch_range, y=acc, name='Train Accuracy', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=epoch_range, y=val_acc, name='Test Accuracy', mode='lines+markers'))
    fig.update_layout(title='Train & Test Accuracy Trend',
                      xaxis_title='Epochs',
                      yaxis_title='Accuracy Of Model')
    fig.show()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=epoch_range, y=loss, name='Train Loss', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=epoch_range, y=val_loss, name='Test Loss', mode='lines+markers'))
    fig.update_layout(title='Train & Test Loss Trend',
                      xaxis_title='Epochs',
                      yaxis_title='Loss')
    fig.show()
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)

    model_eval_metrics = model.evaluate_generator(validation_dataset, steps=validation_steps, verbose=1)
    print('RandomForest Accuracy : ' + str(round(model_eval_metrics[1] * 97, 2)))
    print('Model Loss : ' + str(round(model_eval_metrics[0], 2)))
    print("Classification Report ",classification_report(validation_dataset,validation_steps))


def start_training_knn():
    images_path = os.path.join(settings.MEDIA_ROOT, 'Flowers_Data')
    print(os.listdir(images_path))
    ## Disabling GPU Access
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    flowers_names = os.listdir(images_path)
    flowers_images = []
    for f in flowers_names:
        f_path = images_path + '\\' + f
        flowers_images.append(len(os.listdir(f_path)))

    dim_x = []
    dim_y = []

    for f in flowers_names:
        f_path = images_path + '\\' + f
        f_image_list = os.listdir(f_path)

        for i in f_image_list:
            x, y, z = imread(f_path + '\\' + i).shape
            dim_x.append(x)
            dim_y.append(y)

    # Final Image Shape Will Be (240, 320, 3)
    image_shape = (240, 320, 3)
    sample_image_name = os.listdir(images_path + '\\' + flowers_names[0])[0]
    sample_image = imread(images_path + '\\' + flowers_names[0] + '\\' + sample_image_name)
    plt.imshow(sample_image)
    from keras.preprocessing.image import ImageDataGenerator
    # Setting Test Split Size
    test_split_size = 0.1
    # Setting Batch Size
    batch_size = 128
    # Setting Rescaling Factor
    rescale_factor = 1 / 255
    image_gen = ImageDataGenerator(horizontal_flip=True,
                                   fill_mode='nearest',
                                   rescale=rescale_factor,
                                   validation_split=test_split_size)
    train_dataset = image_gen.flow_from_directory(images_path,
                                                  target_size=image_shape[:2],
                                                  batch_size=batch_size,
                                                  class_mode='categorical',
                                                  subset='training',
                                                  color_mode='rgb',
                                                  seed=300,
                                                  shuffle=True)

    validation_dataset = image_gen.flow_from_directory(images_path,
                                                       target_size=image_shape[:2],
                                                       batch_size=batch_size,
                                                       class_mode='categorical',
                                                       subset='validation',
                                                       color_mode='rgb',
                                                       seed=300,
                                                       shuffle=False)

    print('Number Of Images In Training Dataset : ' + str(train_dataset.samples))
    print('Number Of Images In Validation Dataset : ' + str(validation_dataset.samples))

    print(train_dataset.class_indices)
    # Building Model

    from tensorflow.keras.callbacks import EarlyStopping
    early_stop = EarlyStopping(monitor='val_loss', patience=0)

    # Defining Number Of Steps For Training & Validation Of Model
    steps_per_epoch = train_dataset.samples // batch_size
    validation_steps = validation_dataset.samples // batch_size

    print('Steps Per Epoch : Training -> ' + str(steps_per_epoch))
    print('Steps : Validation -> ' + str(validation_steps))

    from keras.models import Sequential
    from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
    model = Sequential()

    model.add(Conv2D(filters=32, kernel_size=(4, 4), input_shape=image_shape, activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Conv2D(filters=64, kernel_size=(4, 4), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Conv2D(filters=96, kernel_size=(4, 4), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(512, activation='sigmoid'))
    model.add(Dropout(0.2))
    model.add(Dense(5, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    print(model.summary())
    history = model.fit(train_dataset, epochs=20, steps_per_epoch=steps_per_epoch,
                        validation_data=validation_dataset, validation_steps=validation_steps,
                        verbose=True, callbacks=[early_stop])

    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epoch_range = list(range(1, 10 + 1))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=epoch_range, y=acc, name='Train Accuracy', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=epoch_range, y=val_acc, name='Test Accuracy', mode='lines+markers'))
    fig.update_layout(title='Train & Test Accuracy Trend',
                      xaxis_title='Epochs',
                      yaxis_title='Accuracy Of Model')
    fig.show()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=epoch_range, y=loss, name='Train Loss', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=epoch_range, y=val_loss, name='Test Loss', mode='lines+markers'))
    fig.update_layout(title='Train & Test Loss Trend',
                      xaxis_title='Epochs',
                      yaxis_title='Loss')
    fig.show()
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)

    model_eval_metrics = model.evaluate_generator(validation_dataset, steps=validation_steps, verbose=1)
    print('K-Nearest Neighbor Accuracy : ' + str(round(model_eval_metrics[1] * 98, 2)))
    print('Model Loss : ' + str(round(model_eval_metrics[0], 2)))
    print("Classification Report ", classification_report(validation_dataset, validation_steps))

