import os
import socket
import logging
import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, render_template, request
from mnist.training_model import convolutional_model
from mnist.training_model import softmax_regression_model
from redis import Redis, RedisError
from flask_bootstrap import Bootstrap
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

bootstrap = Bootstrap()
bootstrap.init_app(app)

x = tf.placeholder(tf.float32, [None, 784])
sess = tf.Session()

# checkpoint_path = 'mnist/data/convolutional.ckpt'
# reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
# var_to_shape_map = reader.get_variable_to_shape_map()
# for key in var_to_shape_map:
#     print("tensor_name: ", key)
#     print(reader.get_tensor(key))

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
    print(input)
    print(result)
    return result


def convolutional(input):
    return sess.run(y2, feed_dict={x: input, keep_prob: 1.0}).flatten().tolist()


#
# # log = logging.getLogger()
# # log.setLevel('INFO')
# # handler = logging.StreamHandler()
# # handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
# # log.addHandler(handler)
# #
# # KEYSPACE = "mykeyspace"
# #
# #

@app.route("/api/mnist", methods=['post'])
def mnist():
    input = ((255 - np.array(request.json, dtype=np.uint8)) / 255.0).reshape(1, 784)
    output1 = regression(input)
    output2 = convolutional(input)
    return jsonify(results=[output1, output2])


#
# # def hello():
# #     try:
# #         visits = redis.incr("counter")
# #     except RedisError:
# #         visits = "<i>cannot connect to Redis, counter disabled</i>"
# #
# #     html = "<h3>Hello {name}!</h3>" \
# #            "<b>Hostname:</b> {hostname}<br/>" \
# #            "<b>Visits:</b> {visits}"
# #     return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)
# #
# #
# # def createKeySpace():
# #     cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
# #     session = cluster.connect()
# #
# #     log.info("Creating keyspace...")
# #     try:
# #         session.execute("""
# #             CREATE KEYSPACE %s
# #             WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
# #             """ % KEYSPACE)
# #
# #         log.info("setting keyspace...")
# #         session.set_keyspace(KEYSPACE)
# #
# #         log.info("creating table...")
# #         session.execute("""
# #             CREATE TABLE mytable (
# #                 mykey text,
# #                 col1 text,
# #                 col2 text,
# #                 PRIMARY KEY (mykey, col1)
# #             )
# #             """)
# #     except Exception as e:
# #         log.error("Unable to create keyspace")
# #         log.error(e)
# #

@app.route('/')
def main():
    return render_template('index.html', range=range(0, 10))


if __name__ == "__main__":
    app.debug = False
    app.run(host='0.0.0.0', port=8000)
