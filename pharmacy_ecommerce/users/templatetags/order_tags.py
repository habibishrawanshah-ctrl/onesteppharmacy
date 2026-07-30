from django import template

register = template.Library()

STATUS_ORDER = ['pending', 'confirmed', 'processing', 'shipped', 'delivered']
STATUS_LABELS = {
    'pending': 'Pending',
    'confirmed': 'Confirmed',
    'processing': 'Processing',
    'shipped': 'Shipped',
    'delivered': 'Delivered',
}


@register.filter
def order_status_index(status):
    try:
        return STATUS_ORDER.index(status)
    except ValueError:
        return -1


@register.filter
def status_step_class(status, step_index):
    try:
        current_idx = STATUS_ORDER.index(status)
    except ValueError:
        return ''
    if current_idx == step_index:
        return 'active'
    if current_idx > step_index:
        return 'completed'
    return ''


@register.filter
def status_dot_color(status, step_index):
    try:
        current_idx = STATUS_ORDER.index(status)
    except ValueError:
        return '#e5e7eb'
    if current_idx > step_index:
        return '#22c55e'
    if current_idx == step_index:
        return '#0066cc'
    return '#e5e7eb'


@register.filter
def status_dot_icon(status, step_index):
    try:
        current_idx = STATUS_ORDER.index(status)
    except ValueError:
        return '&#9679;'
    if step_index == 0:
        return '&#9679;'
    if current_idx > step_index:
        return '&#10003;'
    if current_idx == step_index:
        return '&#9679;'
    return '&#9679;'


@register.filter
def status_dot_color_icon(status, step_index):
    try:
        current_idx = STATUS_ORDER.index(status)
    except ValueError:
        return ('#e5e7eb', '#9ca3af', '&#9679;')
    if step_index == 0:
        if current_idx == 0:
            return ('#0066cc', 'white', '&#9679;')
        if current_idx > 0:
            return ('#22c55e', 'white', '&#10003;')
        return ('#e5e7eb', '#6b7280', '&#9679;')
    if current_idx > step_index:
        return ('#22c55e', 'white', '&#10003;')
    if current_idx == step_index:
        return ('#0066cc', 'white', '&#9679;')
    return ('#e5e7eb', '#9ca3af', '&#9679;')
