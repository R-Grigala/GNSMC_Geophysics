from flask_restx import Resource
from werkzeug.exceptions import NotFound

from src.api.nsmodels import geophysical_ns, geophysical_model, geophysic_seismic_ns, geophysic_seismic_model, geophysic_logging_ns, geophysic_logging_model
from src.api.nsmodels import geophysic_electrical_ns, geophysic_electrical_model
from src.models import Geophysical, GeophysicSeismic, GeophysicLogging, GeophysicElectrical


@geophysical_ns.route('/geophysical/<int:proj_id>')
@geophysical_ns.doc(responses={200: 'OK', 404: 'Geophysical not found'})
class GeophysicalListAPI(Resource):

    @geophysical_ns.marshal_with(geophysical_model)
    def get(self, proj_id):
        geophysical = Geophysical.query.filter_by(project_id=proj_id).all()
        if not geophysical:
            raise NotFound("Geophysical not found")
        
        return geophysical, 200

@geophysic_seismic_ns.route('/geophysic_seismic/<int:geophy_id>')
class GeophysicSeismicAPI(Resource):
    @geophysic_seismic_ns.marshal_with(geophysic_seismic_model)
    def get(self, geophy_id):
        geophysic_seismic = GeophysicSeismic.query.filter_by(geophysical_id=geophy_id).all()
        if not geophysic_seismic:
            raise NotFound("Geophysical not found")
        
        return geophysic_seismic, 200
    
@geophysic_logging_ns.route('/geophysic_logging/<int:geophy_id>')
class GeophysicLoggingAPI(Resource):
    @geophysic_logging_ns.marshal_with(geophysic_logging_model)
    def get(self, geophy_id):
        geophysic_logging = GeophysicLogging.query.filter_by(geophysical_id=geophy_id).all()
        if not geophysic_logging:
            raise NotFound("Geophysical not found")
        
        return geophysic_logging, 200
    
@geophysic_electrical_ns.route('/geophysic_electrical/<int:geophy_id>')
class GeophysicElectricalAPI(Resource):
    @geophysic_electrical_ns.marshal_with(geophysic_electrical_model)
    def get(self, geophy_id):
        geophysic_electrical = GeophysicElectrical.query.filter_by(geophysical_id=geophy_id).all()
        if not geophysic_electrical:
            raise NotFound("Geophysical not found")
        
        return geophysic_electrical, 200