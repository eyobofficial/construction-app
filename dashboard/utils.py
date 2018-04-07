def status_label(**kwargs):
    btn = kwargs.get('btn', 'btn-default')
    status_message = kwargs.get('status', 'Not Available')
    output = '<span class="badge {}">{}</span>'.format(
        btn,
        status_message,
    )
    return output


def check_project_perm(user, project, perm):
    return project in user.projects_administered.all() and user.has_perm(perm)
