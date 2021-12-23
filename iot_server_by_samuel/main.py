from flask import Flask, jsonify
from flask import render_template
import rcm

app = Flask(__name__)
app.config['DEBUG'] = True
@app.route("/")
def index():
    return render_template('index.html', test="hihihi")


@app.route('/test_api/', methods=['GET'])
def test_api():
    return jsonify(message='Hello, API')


@app.route('/get_data/', methods=['GET'])
def get_data():

    with open("./rcm/data","r") as file:
        data = file.read()
        print(data)

    return data


print(rcm.execute())


'''
if __name__ == "__main__":
    app.run(port=5000,debug=True, host='0.0.0.0')
'''
