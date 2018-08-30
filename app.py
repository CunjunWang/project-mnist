import numpy as np
import tensorflow as tf
from flask_bootstrap import Bootstrap
from flask import Flask, jsonify, render_template, request, url_for
from mnist.training_model import convolutional_model
from mnist.training_model import softmax_regression_model
from database.cassandraSetup import cassandra_setup
from database.cassandraHandler import save_to_cassndra

app = Flask(__name__, static_folder="./static")

# use bootstrap for UI
bootstrap = Bootstrap()
bootstrap.init_app(app)

x = tf.placeholder(tf.float32, [None, 784])
sess = tf.Session()

with tf.variable_scope("softmax_regression"):
    y1, variables = softmax_regression_model.softmax_regression(x)
saver = tf.train.Saver(variables)
saver.restore(sess, "mnist/data/softmax_regression.ckpt")

with tf.variable_scope("convolutional"):
    keep_prob = tf.placeholder(tf.float32)
    y2, variables = convolutional_model.convolutional(x, keep_prob)
saver = tf.train.Saver(variables)
saver.restore(sess, "mnist/data/convolutional.ckpt")


def regression(input_data):
    result = sess.run(y1, feed_dict={x: input_data}).flatten().tolist()
    return result


def convolutional(input_data):
    return sess.run(y2, feed_dict={x: input_data, keep_prob: 1.0}).flatten().tolist()


@app.route('/', methods=['get'])
def main():
    main_css = url_for('static', filename='css/main.css')
    return render_template('./index.html', range=range(0, 10), mainCSS=main_css)


@app.route("/mnist", methods=['post'])
def mnist_main():
    input_data = ((255 - np.array(request.json, dtype=np.uint8)) / 255.0).reshape(1, 784)
    regression_output = regression(input_data)
    convolution_output = convolutional(input_data)
    return jsonify(results=[regression_output, convolution_output])


@app.route("/save", methods=['post'])
def save_data():
    received_data = request.json
    if received_data['predictionData'] is not '':
        save_to_cassndra(received_data)
    return "get data"


if __name__ == "__main__":
    cassandra_setup()
    app.run(host='0.0.0.0', port=8004)
