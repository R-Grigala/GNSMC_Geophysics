from flask_restx import Resource
from werkzeug.exceptions import NotFound

from src.api.nsmodels import geophysic_logging_ns, geophysic_logging_model
from src.models import GeophysicLogging

@geophysic_logging_ns.route('/geophysic_logging/<int:geophy_id>')
class GeophysicLoggingAPI(Resource):
    @geophysic_logging_ns.marshal_with(geophysic_logging_model)
    def get(self, geophy_id):
        geophysic_logging = GeophysicLogging.query.filter_by(geophysical_id=geophy_id).all()
        if not geophysic_logging:
            raise NotFound("Geophysical not found")
        
        return geophysic_logging, 200