import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

# Disable sceintifc notation clarity  명확성을 위해 과학적 표기법 사용 안 함
np.set_printoptions(suppress=True)

# load the model

model = tensorflow.keras.models.load_model('keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'Length' or number of images you can put into the array is 
# determined by the first position in the shape tuple, in this case 1

data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# replace this with the path to your image
image = Image.open('/Users/sup/photo.jpg')

# resize the image to a 224x224 with the same strategy as in TM2:
# resizing the image to be at least 224 x 224 and then cropping from the center
size = (224, 224)
image = ImageOps.fit(image, size, Image.ANTIALIAS)

# turn the image into a numpy array
image_array = np.asarray(image)

# display the resized image
image.show()

# Nomarlized the image
normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

# Load the image into the array
data[0] = normalized_image_array

# run the inference
prediction = model.predict(data)
print(prediction)


