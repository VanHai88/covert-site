from django import template
register = template.Library()

@register.simple_tag
def course_session(course, sess_dict):
    try:
        return sess_dict[course.id].strftime("%e %b, %Y")
    except:
        return 'TBD'

@register.simple_tag
def sort_courses(courses):
    return list(sorted(courses, key=lambda x: x['session'][4]))