import os
import tensorflow as tf
from mnist.training_model import convolutional_model
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

with tf.variable_scope("convolutional"):
    # First arg: type; Second arg: tensor
    # x is a placeholder, represent the image to be recognized
    # None means this dimension is arbitrary (number of input images)
    x = tf.placeholder(tf.float32, [None, 784])
    keep_prob = tf.placeholder(tf.float32)
    y_conv, variables = convolutional_model.convolutional(x, keep_prob)

# training process
y_ = tf.placeholder(tf.float32, [None, 10])
cross_entrophy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entrophy)
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

saver = tf.train.Saver(variables)

with tf.Session() as sess:
    merged_summary_op = tf.summary.merge_all()
    summary_writer = tf.summary.FileWriter('/tmp/mnist_log/1', sess.graph)
    summary_writer.add_graph(sess.graph)
    sess.run(tf.global_variables_initializer())

    for i in range(30000):
        batch = mnist.train.next_batch(50)
        if i % 100 == 0:
            train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
            print("step %d, training accuracy %g" % (i, train_accuracy))
        sess.run(train_step, feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

    print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))

    path = saver.save(
        sess, os.path.join(os.path.dirname(__file__), 'data', 'convolutional.ckpt'),
        write_meta_graph=False, write_state=False)

    print("Saved: ", path)