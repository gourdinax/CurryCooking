from flask import Flask, render_template, request, redirect, url_for
import requests

flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return render_template('index.html')

@flask_app.route('/get_predictions', methods=['POST'])
def get_predictions():
    minutes = float(request.form['minutes'])
    three_point_attempts = float(request.form['three_point_attempts'])
    opponent = request.form['opponent']
    
    response = requests.get("http://127.0.0.1:8001/model", params={
        "minutes": minutes,
        "three_point_attempts": three_point_attempts,
        "opponent": opponent
    })
    
    if response.status_code == 200:
        data = response.json()
        local_prediction = data['local_prediction']
        openai_prediction = data['openai_prediction']
        return render_template('results.html', local_result=local_prediction, openai_result=openai_prediction)
    else:
        return f"Failed to get prediction: {response.json()['detail']}", 400

@flask_app.route('/train_model', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        response = requests.post("http://127.0.0.1:8001/train_model", files={'file': (file.filename, file.stream, file.content_type)})
        if response.status_code == 200:
            return redirect(url_for('index'))
        else:
            return f"Failed to train model: {response.json()['detail']}", 400
    return redirect(url_for('index'))

if __name__ == "__main__":
    flask_app.run(port=5000)
