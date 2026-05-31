from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from ...services.TaskService import TaskService

task_bp = Blueprint('task', __name__, static_folder='../../static', template_folder='../../templates')


@task_bp.route('/')
@login_required
def tasks():
    try:
        tasks = TaskService.get_tasks_assigned_to_user(current_user.id)
    except ValueError as e:
        print(f'ValueError in {__name__}: {e}')
        flash('Server error.', category='error')
        tasks = []

    return render_template('tasks.html', tasks=tasks)


@task_bp.route('/<int:id>', methods=['GET', 'POST'])
def task(id):
    try:
        task = TaskService.get_task(id)
    except ValueError:
        flash('Task not found', category='error')
        return redirect(url_for('task.tasks'))
    except Exception as e:
        print(f'Error occured in {__name__}: {e}')
        flash('Server error.', category='error')
        return redirect(url_for('task.tasks'))

    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Log in to edit tasks.', category='error')
            return redirect(url_for('auth.login'))

        try:
            data = TaskService.build_update_data(request.form)
            task = TaskService.update_task(id, data)
            flash('Task updated.', category='success')
        except ValueError as e:
            flash(str(e), category='error')

    return render_template(
        'task.html',
        task=task,
        statuses=TaskService.get_all_statuses(),
        priorities=TaskService.get_all_priorities(),
    )
