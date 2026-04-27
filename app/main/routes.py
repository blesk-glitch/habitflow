from flask import render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app import db
from app.models import Task, Completion
from app.forms import TaskForm
from . import bp


@bp.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            priority=form.priority.data,
            author=current_user
        )
        db.session.add(task)
        db.session.commit()
        flash('Задача создана!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('task_form.html', form=form)

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks)

@bp.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html')

@bp.route('/task/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    if task.author != current_user:
        abort(403)  # запрет на редактирование чужих задач
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.priority = form.priority.data

        # обработка картинки
        db.session.commit()
        flash('Задача обновлена!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('task_form.html', form=form, task=task)

@bp.route('/task/<int:id>/delete', methods=['POST'])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.author != current_user:
        abort(403)

    from app.models import Completion
    Completion.query.filter_by(task_id=task.id).delete()
    db.session.delete(task)
    db.session.commit()
    flash('Задача удалена.', 'danger')
    return redirect(url_for('main.dashboard'))

@bp.route('/task/<int:id>/complete', methods=['POST'])
@login_required
def complete_task(id):
    task = Task.query.get_or_404(id)
    if task.author != current_user:
        abort(403)
    if not task.is_done:
        task.is_done = True

        # Начисляем +10 за задачу
        current_user.points = (current_user.points or 0) + 10

        from app.models import Completion
        completion = Completion(task_id=task.id)
        db.session.add(completion)
        db.session.commit()
        flash(f'Задача "{task.title}" выполнена! +10 очков.', 'success')
    else:
        flash('Задача уже выполнена.', 'info')
    return redirect(url_for('main.dashboard'))