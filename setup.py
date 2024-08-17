
# GET /tasks: Retrieve all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})
=======
def find_task(task_id):
    return next((task for task in tasks if task['id'] == task_id), None)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = find_task(id)
    if task is None:
        logging.error(f'Task with id {id} not found.')
        abort(404, description="Task not found")
    return jsonify(task)

