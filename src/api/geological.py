from flask_restx import Resource
from werkzeug.exceptions import NotFound

from src.api.nsmodels import geological_ns, geological_model
from src.models import Geological


@geological_ns.route('/geological/<int:proj_id>')
@geological_ns.doc(responses={200: 'OK', 404: 'Geological not found'})
class GeologicalAPI(Resource):

    @geological_ns.marshal_with(geological_model)
    def get(self, proj_id):
        geological = Geological.query.filter_by(project_id=proj_id).all()
        if not geological:
            raise NotFound("Geological not found")
        
        return geological, 200
