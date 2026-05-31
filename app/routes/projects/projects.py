from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from ...services.ProjectService import ProjectService
from ...services.TeamService import TeamService
from ...services.TaskService import TaskService

project_bp = Blueprint('project', __name__, static_folder='../../static', template_folder='../../templates')


@project_bp.route('/')
@login_required
def projects():
    projects = []
    try:
        projects = ProjectService.get_projects(current_user.id)
    except ValueError as e:
        print(f'ValueError in {__name__}: {e}')
        flash('Server error.', category='error')

    return render_template('projects.html', projects=projects)


@project_bp.route('/<int:id>')
@login_required
def project(id):
    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    try:
        project = ProjectService.get_project(id)
        tasks = ProjectService.get_sorted_tasks(id, sort, order)
        members = TeamService.get_project_members(id)
    except ValueError as e:
        print(f'ValueError in {__name__}: {e}')
        flash(str(e), category='error')
        return redirect(url_for('project.projects'))

    return render_template(
        'project.html',
        project=project,
        tasks=tasks,
        members=members,
        sort=sort,
        order=order,
        sorts=ProjectService.get_available_sorts(),
    )


@project_bp.route('/<int:id>/tasks/new', methods=['GET', 'POST'])
@login_required
def new_task(id):
    try:
        project = ProjectService.get_project(id)
    except ValueError as e:
        flash(str(e), category='error')
        return redirect(url_for('project.projects'))

    if request.method == 'POST':
        try:
            TaskService.create_task({
                'name': request.form.get('name'),
                'description': request.form.get('description'),
                'createdBy': current_user.id,
                'projectID': project.id,
                'status': request.form.get('status'),
                'priority': request.form.get('priority'),
                'deadline': TaskService.parse_deadline(request.form.get('deadline')),
            })
            flash('Task created.', category='success')
            return redirect(url_for('project.project', id=project.id))
        except ValueError as e:
            flash(str(e), category='error')

    return render_template(
        'task_form.html',
        project=project,
        statuses=TaskService.get_all_statuses(),
        priorities=TaskService.get_all_priorities(),
        task=None,
    )
