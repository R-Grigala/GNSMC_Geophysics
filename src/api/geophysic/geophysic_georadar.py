from flask_restx import Resource
from werkzeug.exceptions import NotFound

from src.api.nsmodels import geophysic_georadar_ns, geophysic_georadar_model, geophysic_georadar_parser
from src.models import GeophysicGeoradar

@geophysic_georadar_ns.route('/geophysic_georadar/<int:geophy_id>')
class GeophysicGeoradarListAPI(Resource):
    @geophysic_georadar_ns.marshal_with(geophysic_georadar_model)
    def get(self, geophy_id):
        geophysic_georadar = GeophysicGeoradar.query.filter_by(geophysical_id=geophy_id).all()
        if not geophysic_georadar:
            raise NotFound("GeophysicGeoradar not found")
        
        return geophysic_georadar, 200