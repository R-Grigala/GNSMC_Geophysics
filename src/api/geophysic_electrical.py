from flask_restx import Resource
from werkzeug.exceptions import NotFound

from src.api.nsmodels import geophysic_electrical_ns, geophysic_electrical_model
from src.models import GeophysicElectrical

@geophysic_electrical_ns.route('/geophysic_electrical/<int:geophy_id>')
class GeophysicElectricalAPI(Resource):
    @geophysic_electrical_ns.marshal_with(geophysic_electrical_model)
    def get(self, geophy_id):
        geophysic_electrical = GeophysicElectrical.query.filter_by(geophysical_id=geophy_id).all()
        if not geophysic_electrical:
            raise NotFound("Geophysical not found")
        
        return geophysic_electrical, 200