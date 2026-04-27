from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Task

bp = Blueprint('api', __name__)

@bp.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'due_date': t.due_date.isoformat(),
        'is_done': t.is_done,
        'priority': t.priority,
        'description': t.description
    } for t in tasks])

@bp.route('/tasks', methods=['POST'])
@login_required
def create_task():
    data = request.get_json()
    task = Task(title=data['title'], due_date=data['due_date'], author=current_user)
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task created', 'id': task.id}), 201