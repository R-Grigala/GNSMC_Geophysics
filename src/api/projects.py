from flask_restx import Resource
from werkzeug.exceptions import NotFound
from datetime import datetime

from src.api.nsmodels import projects_ns, projects_model, projects_parser
from src.models import Projects


@projects_ns.route('/projects')
@projects_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class ProjectsListAPI(Resource):

    @projects_ns.marshal_list_with(projects_model)
    def get(self):
        projects = Projects.query.all()

        return projects, 200
    
    @projects_ns.expect(projects_parser)
    def post(self):
        args = projects_parser.parse_args()
        
        try:
            start_time = datetime.strptime(args['start_time'], '%Y-%m-%d').date()
            end_time = datetime.strptime(args['end_time'], '%Y-%m-%d').date()
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400

        new_project = Projects(
            projects_name=args['projects_name'],
            contract_number=args['contract_number'],
            start_time=start_time,
            end_time=end_time,
            contractor=args['contractor'],
            proj_location=args['proj_location'],
            proj_latitude=args['proj_latitude'],
            proj_longitude=args['proj_longitude'],
            geological_study=args['geological_study'],
            geophysical_study=args['geophysical_study'],
            hazard_study=args['hazard_study'],
            geodetic_study=args['geodetic_study'],
            other_study=args['other_study']
        )
        new_project.create()

        return {"message": "Successfully created Project"}, 200
    
@projects_ns.route('/project/<int:id>')
@projects_ns.doc(responses={200: 'OK', 404: 'Project not found'})
class ProjectAPI(Resource):

    @projects_ns.marshal_with(projects_model)
    def get(self, id):
        project = Projects.query.get(id)
        if not project:
            raise NotFound("Project not found")
        
        return project, 200
    
    @projects_ns.expect(projects_parser)
    def put(self, id):
        args = projects_parser.parse_args()
        try:
            start_time = datetime.strptime(args['start_time'], '%Y-%m-%d').date()
            end_time = datetime.strptime(args['end_time'], '%Y-%m-%d').date()
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400

        project = Projects.query.get(id)
        if project:
            project.projects_name = args["projects_name"]
            project.contract_number = args["contract_number"]
            project.start_time = start_time
            project.end_time = end_time
            project.contractor=args['contractor']
            project.proj_location = args["proj_location"]
            project.proj_latitude = args["proj_latitude"]
            project.proj_longitude = args["proj_longitude"]
            project.geological_study = args["geological_study"]
            project.geophysical_study = args["geophysical_study"]
            project.hazard_study = args["hazard_study"]
            project.geodetic_study = args["geodetic_study"]
            project.other_study = args["other_study"]
            project.save()  
            return {"message": "Successfully updated Project"}, 200
        else:
            raise NotFound("Project not found")

    def delete(self, id):
        project = Projects.query.get(id)
        if project:
            project.delete()
            return {"message": "Successfully deleted Project"}, 200
        else:
            raise NotFound("Project not found")

