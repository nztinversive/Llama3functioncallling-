from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# Basic Q&A and facts database
facts_db = {
    "sun": "The sun is a star at the center of the Solar System.",
    "moon": "The moon is Earth's only natural satellite.",
    "earth": "Earth is the third planet from the Sun."
}

# To-Do list storage
todo_list = []

def simple_answer(query):
    """Provides simple answers based on the query."""
    query = query.lower().strip()
    return facts_db.get(query, "Sorry, I don't know that. Ask me another question!")

@app.route('/ask', methods=['GET'])
def ask():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Missing query'}), 400
    answer = simple_answer(query)
    return jsonify({'response': answer})

@app.route('/todo', methods=['GET', 'POST', 'DELETE'])
def manage_todo():
    if request.method == 'POST':
        task = request.json.get('task', '')
        if task:
            todo_list.append({'task': task, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            return jsonify({'result': 'Task added', 'task': task}), 201
        return jsonify({'error': 'Missing task in request'}), 400
    elif request.method == 'DELETE':
        task = request.args.get('task', '')
        if task and {'task': task} in todo_list:
            todo_list.remove({'task': task})
            return jsonify({'result': 'Task removed', 'task': task}), 200
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'todo_list': todo_list})

@app.route('/calculate', methods=['GET'])
def calculate():
    try:
        expression = request.args.get('expression', '')
        result = eval(expression)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
