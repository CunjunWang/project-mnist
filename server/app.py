import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, render_template, request, url_for
from mnist.training_model import convolutional_model
from mnist.training_model import softmax_regression_model
from flask_bootstrap import Bootstrap

# cassandra file
import logging
from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement

#

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

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
    # print(input)
    # print(result)
    return result


def convolutional(input):
    return sess.run(y2, feed_dict={x: input, keep_prob: 1.0}).flatten().tolist()


@app.route('/', methods=['get'])
def main():
    mainCSS = url_for('static', filename='css/main.css')
    return render_template('index.html', range=range(0, 10), mainCSS=mainCSS)


@app.route("/mnist", methods=['post'])
def mnist():
    input = ((255 - np.array(request.json, dtype=np.uint8)) / 255.0).reshape(1, 784)
    output1 = regression(input)
    output2 = convolutional(input)
    return jsonify(results=[output1, output2])


@app.route("/react")
def index():
    return render_template("index.html")


# cassandra file
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

KEYSPACE = "MNISTSpace"

cluster = Cluster(contact_points=['127.0.0.1'])
session = cluster.connect()

spacenames = list(map(lambda space: space.keyspace_name, session.execute("SELECT * FROM system_schema.keyspaces")))


def setUp():
    createKeySpace()
    createTable()


def createKeySpace():
    log.info("run create key space")
    try:
        log.info("Creating Keyspace...")

        if KEYSPACE not in spacenames:
            log.info("Keyspace %s does not exist, creating..." % KEYSPACE)
            session.execute("""
                CREATE KEYSPACE %s WITH replication = 
                { 'class': 'SimpleStrategy', 'replication_factor': '2' }
                """ % KEYSPACE)
            log.info("Keyspace %s created successfully." % KEYSPACE)
        else:
            log.info("Keyspace %s already existed." % KEYSPACE)

        log.info("Setting Keyspace...")
        session.set_keyspace(KEYSPACE)
        session.execute('use %s' % KEYSPACE)
    except Exception as e:
        log.error("Unable to create keyspace.")
        log.error(e)


def createTable():
    log.info("run create table")
    tablename = "%s.MNISTDataTable" % KEYSPACE
    session.execute("""CREATE TABLE IF NOT EXISTS %s 
        (id int PRIMARY KEY, img_data text, prediction text, create_time DATE)
        """ % tablename)


#

if __name__ == "__main__":
    setUp()
    app.run(host='0.0.0.0', port=8004)
