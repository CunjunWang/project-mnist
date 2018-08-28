import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, render_template, request, url_for
from mnist.training_model import convolutional_model
from mnist.training_model import softmax_regression_model
from flask_bootstrap import Bootstrap
from server.cassandraSetup import setUp
from client import drawer

app = Flask(__name__, static_folder="../static", template_folder="../templates")

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


def regression(input):
    result = sess.run(y1, feed_dict={x: input}).flatten().tolist()
    return result


def convolutional(input):
    return sess.run(y2, feed_dict={x: input, keep_prob: 1.0}).flatten().tolist()


@app.route('/', methods=['get'])
def main():
    mainCSS = url_for('static', filename='css/main.css')
    return render_template('index.html', range=range(0, 10), mainCSS=mainCSS)


@app.route("/mnist", methods=['post'])
def mnist():
    # print("mnist request is: %s" % request.json)
    input_data = ((255 - np.array(request.json, dtype=np.uint8)) / 255.0).reshape(1, 784)
    output1 = regression(input_data)
    output2 = convolutional(input_data)
    # print('input 1 from python: %s' % output1)
    # print('input 2 from python: %s' % output2)
    return jsonify(results=[output1, output2])


@app.route("/save", methods=['post'])
def saveData():
    return


@app.route("/react")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    setUp()
    drawer.Drawer()
    app.run(host='0.0.0.0', port=8004)
