import os
import tensorflow as tf
from mnist.training_model import softmax_regression_model
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

with tf.variable_scope("softmax_regression"):
    # First arg: type; Second arg: tensor
    # x is a placeholder, represent the image to be recognized
    # None means this dimension is arbitrary (number of input images)
    x = tf.placeholder(tf.float32, [None, 784])
    y, variables = softmax_regression_model.softmax_regression(x)

# training process
# y_ is the real label of image
y_ = tf.placeholder(tf.float32, [None, 10])
# introduce the cross entrophy
cross_entrophy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y)))
# use gradient descent to reduce the loss; 0.01 is learning rate
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entrophy)
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

saver = tf.train.Saver(variables)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for _ in range(10000):
        # fetch 1000 training data in training set
        # batch_xs size (100, 784), batch_ys size (100, 10)
        batch_xs, batch_ys = mnist.train.next_batch(100)
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

    print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

    path = saver.save(
        sess, os.path.join(os.path.dirname(__file__), 'data', 'softmax_regression.ckpt'),
        write_meta_graph=False, write_state=False)

    print("Saved: ", path)
