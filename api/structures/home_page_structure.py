from flask_restful import fields


resource_structure = {
        'url': fields.String,
        'description': fields.String
        }
resources_structure = {
        'resource': fields.Nested(resource_structure)
        }
home_page_structure = {
        'endpoints': fields.List(fields.Nested(resources_structure))
        }
