from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage: a simple list to hold our tasks
tasks = []
next_id = 1

# Endpoint 1: Add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    global next_id
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Request body must be a JSON object'}), 400

    title = data.get('title')
    if not isinstance(title, str) or not title.strip():
        return jsonify({'error': 'title is required and must be a non-empty string'}), 400

    task = {
        'id': next_id,
        'title': title.strip(),
        'done': False
    }
    tasks.append(task)
    next_id += 1
    return jsonify(task), 201

# Endpoint 2: List all tasks
@app.route('/tasks', methods=['GET'])
def list_tasks():
    return jsonify(tasks), 200

# Endpoint 3: Mark a task as done
@app.route('/tasks/<int:task_id>/done', methods=['PUT'])
def mark_done(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = True
            return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

@app.errorhandler(404)
def not_found(_error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(405)
def method_not_allowed(_error):
    return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)