from restless.models import serialize

# api.py: return a valid page JSON object included course and sections
def serialize_page(page, course):
    return serialize(page, include=[
        (
            'course', lambda a: {
                'id': course.id,
                'name': course.name, 
                'description': course.description,
                'percentage': course.percentage(),
                'published': course.published
            }
        ),
            ('sections', dict()),
            ('total_pages', lambda a: course.total_pages()),
            ('progression', lambda a: a.state()),
        ])