from flask import Flask, jsonify, request, abort
from datetime import datetime
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)

# In-memory data storage
tasks = []
task_id_counter = 1

# Task model (in-memory storage)
def create_task(title, description, status):
    global task_id_counter
    task = {
        'id': task_id_counter,
        'title': title,
        'description': description,
        'status': status,
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    tasks.append(task)
    task_id_counter += 1
    return task

# Helper function to find a task by id
def find_task(task_id):
    return next((task for task in tasks if task['id'] == task_id), None)

# GET /tasks: Retrieve all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# GET /tasks/<id>: Retrieve a specific task
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = find_task(id)
    if task is None:
        logging.error(f'Task with id {id} not found.')
        abort(404, description="Task not found")
    return jsonify(task)

# POST /tasks: Create a new task
@app.route('/tasks', methods=['POST'])
def create_task_endpoint():
    if not request.json or not 'title' in request.json:
        logging.error('Invalid input for creating a task.')
        abort(400, description="Invalid input")
    
    title = request.json['title']
    description = request.json.get('description', "")
    status = request.json.get('status', "pending")
    
    task = create_task(title, description, status)
    logging.info(f'Task created with id {task["id"]}')
    return jsonify(task), 201

# PUT /tasks/<id>: Update an existing task
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = find_task(id)
    if task is None:
        logging.error(f'Task with id {id} not found for updating.')
        abort(404, description="Task not found")
    
    if not request.json:
        logging.error('Invalid input for updating a task.')
        abort(400, description="Invalid input")
    
    title = request.json.get('title', task['title'])
    description = request.json.get('description', task['description'])
    status = request.json.get('status', task['status'])
    
    task['title'] = title
    task['description'] = description
    task['status'] = status
    task['updated_at'] = datetime.utcnow().isoformat()
    
    logging.info(f'Task with id {id} updated.')
    return jsonify(task)

# DELETE /tasks/<id>: Delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = find_task(id)
    if task is None:
        logging.error(f'Task with id {id} not found for deletion.')
        abort(404, description="Task not found")
    
    tasks.remove(task)
    logging.info(f'Task with id {id} deleted.')
    return jsonify({'result': True})

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': error.description}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': error.description}), 400

if __name__ == '__main__':
    app.run(debug=True)
