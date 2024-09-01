from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.db import execute_query


tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/data', methods=['GET'])
def users():
    query = "SELECT * FROM todolist"
    print(f"Executing query: {query}")  # Debugging line
    data = execute_query(query)
    return jsonify(data)


@tasks_bp.route('/add_task', methods=['POST'])
def add_task():
    data = request.get_json()
    title, name = data.get('title'), data.get('name')
    if not title or not name:
        return jsonify({'message': 'Title and name are required!'})
    query = 'INSERT INTO todolist (title, name) VALUES(%s, %s)'
    execute_query(query, (title, name), commit=True)
    return jsonify({'message': 'Task added successfully'})


@tasks_bp.route('/update_task/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    fields = [f"{key}=%s" for key in data.keys()]
    values = list(data.values())
    if not fields:
        return jsonify({'message': 'No valid fields to update'})
    query = f"UPDATE todolist SET {', '.join(fields)} WHERE id=%s"
    values.append(id)
    try:
        execute_query(query, values, commit=True)
    except Exception as e:
        error_message = str(e)
        if 'Unknown column' in error_message:
            column_name = error_message.split('\'')[1]
            return jsonify({'message': f'Unknown column: {column_name}'})
        return jsonify({'message': 'Database operation error', 'error': error_message})
    return jsonify({'message': 'Task updated successfully'})


@tasks_bp.route('/delete_task/<int:id>', methods=['DELETE'])
def delete_task(id):
    query = "DELETE FROM todolist WHERE id= %s"
    try:
        execute_query(query, (id,), commit=True)
    except Exception as e:
        return jsonify({'message': 'Failed to delete task', 'error': str(e)})
    return jsonify({'message': 'Task deleted successfully'})
