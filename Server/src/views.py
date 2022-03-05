from src import app
from src.models import Model
from flask import request
import simplejson

# initialize the model
model = Model()
print("================================================================")


def json_dumps(data):
    return simplejson.dumps(data, ensure_ascii=False, ignore_nan=True)


@app.route('/get_list', methods=['GET'])
def get_list():
    return json_dumps(model.get_list())


@app.route('/get_filtered_list', methods=['POST'])
def get_filtered_list():
    post_data = request.data.decode()
    if post_data != "":
        post_data = simplejson.loads(post_data)
    return json_dumps(model.get_filtered_list(post_data))