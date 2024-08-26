from flask_restx import Resource
from werkzeug.exceptions import NotFound

from src.api.nsmodels import geophysic_seismic_ns, geophysic_seismic_model
from src.models import GeophysicSeismic

@geophysic_seismic_ns.route('/geophysic_seismic/<int:geophy_id>')
class GeophysicSeismicAPI(Resource):
    @geophysic_seismic_ns.marshal_with(geophysic_seismic_model)
    def get(self, geophy_id):
        geophysic_seismic = GeophysicSeismic.query.filter_by(geophysical_id=geophy_id).all()
        if not geophysic_seismic:
            raise NotFound("Geophysical not found")
        
        return geophysic_seismic, 200