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

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = find_task(id)
    if task is None:
        logging.error(f'Task with id {id} not found for deletion.')
        abort(404, description="Task not found")
    
    tasks.remove(task)
    logging.info(f'Task with id {id} deleted.')
    return jsonify({'result': True})



if __name__ == '__main__':
    app.run(debug=True)
