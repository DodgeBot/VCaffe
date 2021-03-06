import numpy as np
import matplotlib.pyplot as plt
import sys
caffe_root = '../../caffe-master'
sys.path.insert(0, caffe_root + 'python')
import caffe
import os

# GPU
caffe.set_device(0)
caffe.set_mode_gpu()

# CPU
# caffe.set_mode_cpu()

model_def = os.path.join(caffe_root, 'models/fyp/deploy.prototxt')
model_weights = os.path.join(caffe_root, 'models/fyp/fyp_iter_4030.caffemodel')

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

mu = np.load(os.path.join(caffe_root, 'python/caffe/imagenet/ilsvrc_2012_mean.npy'))
mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
print 'mean-subtracted values:', zip('BGR', mu)

# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

# image = caffe.io.load_image('/home/fyp/FYP/fyp_ws/data/170112/left03/frame0.jpg')
image = caffe.io.load_image('/home/fyp/FYP/fyp_ws/data/170112/right01/frame0.jpg')
transformed_image = transformer.preprocess('data', image)
plt.imshow(image)

# copy the image data into the memory allocated for the net
net.blobs['data'].data[...] = transformed_image

### perform classification
output = net.forward()

output_prob = output['prob'][0]  # the output probability vector for the first image in the batch

print ''
print 'predicted class is:', output_prob.argmax()
