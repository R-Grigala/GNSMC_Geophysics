from flask_restx import Resource
from werkzeug.exceptions import NotFound
from datetime import datetime
import os
import uuid
import mimetypes

from src.api.nsmodels import projects_ns, projects_model, projects_parser
from src.models import Projects, Images
from src.config import Config


@projects_ns.route('/projects')
@projects_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class ProjectsListAPI(Resource):

    @projects_ns.marshal_list_with(projects_model)
    def get(self):
        projects = Projects.query.all()

        return projects, 200
    
    @projects_ns.doc(parser=projects_parser)
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
            proj_longitude=args['proj_longitude']
        )
        new_project.create()

        # Handle image uploads
        image_types = ["image/jpeg", "image/png", "image/jpg"]
        
        if not args["images"]:
            return {"message": "No images provided"}, 400

        images_directory = os.path.join(Config.BASE_DIR, 'src', 'images', str(new_project.id))
        os.makedirs(images_directory, exist_ok=True)

        try:
            for image in args["images"]:
                if image.mimetype not in image_types:
                    return {"message": "Invalid image type."}, 400
                
                extension = mimetypes.guess_extension(image.mimetype) or ".jpg"
                file_name = str(uuid.uuid4()) + extension
                image_path = os.path.join(images_directory, file_name)
                
                # Save the file to the directory
                image.save(image_path)
                
                # Save the file path to the database
                new_image = Images(path=file_name, project_id=new_project.id)
                new_image.create()

            return {"message": "Successfully created project with images"}, 200
        
        except OSError as e:
            return {"message": f"Failed to save images: {str(e)}"}, 500
    
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

