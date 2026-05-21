from flask import Blueprint, render_template, flash, redirect
from flask_login import login_required, current_user

from ...model.Tasks import Task
from ...services.TaskService import TaskService

task_bp = Blueprint('task', __name__, static_folder='../../static', template_folder='../../template')


@task_bp.route('/')
@login_required
def tasks():
    try:
        tasks = TaskService.get_tasks_assigned_to_user(current_user.id)
    except ValueError as e:
        print(f'ValueError in {__name__}: {e}')
        flash('Server error.', category='error')
    
    return render_template('tasks.html', tasks=tasks)

@task_bp.route('/<id>')
def task(id):
    try:
        task = TaskService.get_task(id)
    except ValueError:
        flash('Task not found')
        return redirect('tasks.html')
    except Exception as e:
        print(f'Error occured in {__name__}: {e}')
    
    return render_template('task.html', task=task)