import datetime
import uuid


def save_to_cassndra(data_to_save):
    data = {
        # 'id': uuid.uuid1(),
        # 'img': data_to_save.imgData,
        # 'prediction': data_to_save.predictionData,
        # 'timestamp': datetime.datetime.now()
    }
    return data
