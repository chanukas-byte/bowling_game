from flask import Flask, request, jsonify

app = Flask(__name__)
high_scores = []

@app.route('/highscores', methods=['GET'])
def get_highscores():
    return jsonify(sorted(high_scores, reverse=True)[:10])

@app.route('/submit', methods=['POST'])
def submit_score():
    data = request.get_json()
    score = data.get('score')
    if isinstance(score, int):
        high_scores.append(score)
        return jsonify({'status': 'success'}), 201
    return jsonify({'status': 'error', 'message': 'Invalid score'}), 400

if __name__ == '__main__':
    app.run(debug=True)
