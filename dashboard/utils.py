def status_label(**kwargs):
    btn = kwargs.get('btn', 'btn-default')
    status_message = kwargs.get('status', 'Not Available')
    output = '<span class="badge {}">{}</span>'.format(
        btn,
        status_message,
    )
    return output
