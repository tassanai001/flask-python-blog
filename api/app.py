import os
import json
from bson import ObjectId
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask_pymongo import PyMongo
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


class JSONEncoder(json.JSONEncoder):
    def default(self, o):  # pylint: disable=E0202
        print(o)
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)
project_root = os.path.dirname(__file__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["MONGO_URI"] = "mongodb://localhost:27017/myBlog"
mongo = PyMongo(app)
cors = CORS(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET'])
def get_all_blog():
    output = []
    data = mongo.db.blog.find({})
    for s in data:
        id = JSONEncoder().encode(s['_id'])
        replaceString = id.replace('"', '')
        subTitleFormat = s['subtitle']

        if len(subTitleFormat) > 60:
            subTitleFormat = subTitleFormat[0:60] + '...'

        output.append({
            'id': replaceString,
            'title': s['title'],
            'detail': s['detail'],
            'subtitle': subTitleFormat,
            'author': s['author'],
            'img': s.get('img', '1601399329957.jpeg'),
            'created_time': str(s['created_time'])
        })
    return jsonify({'result': output})


@app.route("/detail", methods=['POST'])
def get_detail():
    data = request.get_json()
    if (data.get('id', None) is not None):
        _id = data.get('id', '')
        print(_id)
        payload = mongo.db.blog.find_one_or_404({'_id': ObjectId(_id)})

        id = JSONEncoder().encode(payload['_id'])
        replaceString = id.replace('"', '')

        blog = {
            'id': replaceString,
            'title': payload['title'],
            'detail': payload['detail'],
            'subtitle': payload['subtitle'],
            'author': payload['author'],
            'img': payload.get('img', '1601399329957.jpeg'),
            'created_time': str(payload['created_time'])
        }
        return blog, 200
    else:
        return jsonify({'failed': False, 'message': 'Bad request parameters!'}), 400


@ app.route("/create-blog", methods=['POST'])
def create():
    data = request.get_json()
    if (data.get('title', None) is not None and
        data.get('detail', None) is not None and
        data.get('subtitle', None) is not None and
        data.get('img', None) is not None and
            data.get('author', None) is not None):
        data['created_time'] = datetime.now()
        data['updated_time'] = datetime.now()
        mongo.db.blog.insert_one(data)
        return jsonify({'ok': True, 'message': 'Blog created successfully!'}), 200
    else:
        return jsonify({'failed': False, 'message': 'Bad request parameters!'}), 400


@ app.route("/update-blog", methods=['POST'])
def update():
    data = request.get_json()
    if (data.get('id', None) is not None and
        data.get('title', None) is not None and
        data.get('detail', None) is not None and
        data.get('subtitle', None) is not None and
        data.get('img', None) is not None and
            data.get('author', None)):

        _id = data.get('id', '')
        result = mongo.db.blog.delete_one({'_id': ObjectId(_id)})
        if (result.deleted_count == 1):
            data['created_time'] = datetime.now()
            data['_id'] = ObjectId(_id)
            mongo.db.blog.insert_one(data)
            return jsonify({'ok': True, 'message': 'Blog created successfully!'}), 200
        else:
            return jsonify({'failed': True, 'message': 'Error ' + _id + ' not found!'}), 404
    else:
        return jsonify({'failed': False, 'message': 'Bad request parameters!'}), 400


@ app.route("/delete-blog", methods=['POST'])
def delete():
    data = request.get_json()
    if (data.get('id', None) is not None):
        _id = data.get('id', '')
        result = mongo.db.blog.delete_one({'_id': ObjectId(_id)})
        if (result.deleted_count == 1):
            return jsonify({'ok': True, 'message': 'Blog delete successfully!'}), 200
        else:
            return jsonify({'failed': True, 'message': 'Error ' + _id + ' not found!'}), 404
    else:
        return jsonify({'failed': False, 'message': 'Bad request parameters!'}), 400


@app.route('/uploadimg', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'failed': False, 'message': 'Bad request parameters!'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'failed': False, 'message': 'Bad request parameters!'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'ok': True, 'message': 'Blog created successfully!'}), 200


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
