import datetime
import uuid
from numpy import long
import numpy as np

from database.cassandraSetup import session



def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()


def unix_time_millis(dt):
    return long(unix_time(dt) * 1000.0)


def get_softmax_prediction(data):
    return np.argmax(data['results'][0])


def get_convolution_prediction(data):
    return np.argmax(data['results'][1])


def save_to_cassndra(data_to_save):
    data = {
        'id': str(uuid.uuid1()),
        'softmax_prediction': get_softmax_prediction(data_to_save['predictionData']),
        'convolution_prediction': get_convolution_prediction(data_to_save['predictionData']),
        'timestamp': unix_time_millis(datetime.datetime.now())
    }
    print(data['timestamp'])
    session.execute("""INSERT INTO mnistspace.mnistdatatable(id, softmax_prediction, convolution_prediction, create_time)
        VALUES( %s, %s, %s, %s)""" % (data['id'], data['softmax_prediction'], data['convolution_prediction'], data['timestamp']))
