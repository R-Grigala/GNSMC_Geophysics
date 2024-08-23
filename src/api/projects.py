from flask_restx import Resource
from werkzeug.exceptions import NotFound
from datetime import datetime
import os
import uuid
import mimetypes

from src.api.nsmodels import projects_ns, projects_model, projects_parser, projects_img_model, project_img_parser
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

        # Handle image uploads if provided
        image_types = ["image/jpeg", "image/png", "image/jpg"]
        images = args['images']

        invalid_files = []
        images_saved = False
        images_directory = os.path.join(Config.BASE_DIR, 'src', 'temp', 'projects', 'images', str(new_project.id))
        
        for image in images:
            if image.mimetype not in image_types:
                invalid_files.append(image.filename)
                continue

            if not images_saved:
                os.makedirs(images_directory, exist_ok=True)
                images_saved = True
            
            extension = mimetypes.guess_extension(image.mimetype) or ".jpg"
            file_name = str(uuid.uuid4()) + extension
            image_path = os.path.join(images_directory, file_name)
            
            try:
                # Save the file to the directory
                image.save(image_path)
                
                # Save the file path to the database
                new_image = Images(path=file_name, project_id=new_project.id)
                new_image.create()
            except OSError as e:
                return {"message": f"Failed to save images: {str(e)}"}, 500
        
        if invalid_files:
            return {"message": "პროექტი შეიქმნა, მაგრამ პროექტის სურათი არ აიტვირთა"}, 200
        
        return {"message": "Successfully created project"}, 200
    
@projects_ns.route('/project/<int:id>')
@projects_ns.doc(responses={200: 'OK', 404: 'Project not found'})
class ProjectAPI(Resource):

    @projects_ns.marshal_with(projects_model)
    def get(self, id):
        project = Projects.query.get(id)
        if not project:
            raise NotFound("Project not found")
        
        images = Images.query.filter_by(project_id=id).all()
        project.images = images

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
            # Delete associated images if they exist
            images = Images.query.filter_by(project_id=id).all()
            if images:
                images_directory = os.path.join(Config.BASE_DIR, 'src', 'temp', 'projects', 'images', str(id))
                try:
                    # Delete images from filesystem
                    for image in images:
                        image_path = os.path.join(images_directory, image.path)
                        if os.path.isfile(image_path):
                            os.remove(image_path)
                        
                        # Delete image record from the database
                        image.delete()
                    
                    # Optionally delete the directory if it's empty
                    if os.path.isdir(images_directory) and not os.listdir(images_directory):
                        os.rmdir(images_directory)
                except OSError as e:
                    return {"message": f"Failed to delete images: {str(e)}"}, 500
            
            # Delete the project record from the database
            project.delete()
            return {"message": "Successfully deleted Project and associated images"}, 200
        else:
            raise NotFound("Project not found")
        
@projects_ns.route('/project/<int:proj_id>/images')
@projects_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 404: 'Not Found'})
class ProjectImageListAPI(Resource):

    @projects_ns.marshal_with(projects_img_model)
    def get(self, proj_id):

        # Fetch images associated with the project
        images = Images.query.filter_by(project_id=proj_id).all()
        if not images:
            return {"message": "No images found for this project"}, 404
        
        return images, 200


    @projects_ns.doc(parser=project_img_parser)
    @projects_ns.marshal_with(projects_img_model)
    def post(self, proj_id):
        # Ensure the project exists
        project = Projects.query.get(proj_id)
        if not project:
            return {"message": "Project not found"}, 404

        # Parse arguments
        args = project_img_parser.parse_args()
        images = args['images']
        if not images:
            return {"message": "No images provided"}, 400
        
        # Validate image type and size (if needed)
        image_types = ["image/jpeg", "image/png", "image/jpg"]
        max_image_size = 5 * 1024 * 1024  # 5MB limit (example)

        images_directory = os.path.join(Config.BASE_DIR, 'src', 'temp', 'projects', 'images', str(proj_id))
        os.makedirs(images_directory, exist_ok=True)

        saved_images = []

        try:
            for image in images:
                if image.mimetype not in image_types:
                    return {"message": "Invalid image type."}, 400

                if image.content_length > max_image_size:
                    return {"message": "Image file too large."}, 400

                # Save each image
                extension = mimetypes.guess_extension(image.mimetype) or ".jpg"
                file_name = str(uuid.uuid4()) + extension
                image_path = os.path.join(images_directory, file_name)
                image.save(image_path)

                # Save image record in the database
                new_image = Images(path=file_name, project_id=proj_id)
                new_image.create()
                saved_images.append(new_image)

            return saved_images, 200
        
        except OSError as e:
            return {"message": f"Failed to save images: {str(e)}"}, 500


@projects_ns.route('/project/<int:proj_id>/images/<int:image_id>')
@projects_ns.doc(responses={200: 'OK', 404: 'Not Found'})
class ProjectImageAPI(Resource):

    def delete(self, proj_id, image_id):
        # Find the image record
        image = Images.query.filter_by(id=image_id, project_id=proj_id).first()
        if not image:
            raise NotFound("Image not found")

        # Path to the image file
        images_directory = os.path.join(Config.BASE_DIR, 'src', 'temp', 'projects', 'images', str(proj_id))
        image_path = os.path.join(images_directory, image.path)
        
        try:
            # Delete the image file from the filesystem
            if os.path.isfile(image_path):
                os.remove(image_path)
            
            # Delete the image record from the database
            image.delete()

            # Optionally, delete the directory if it's empty
            if os.path.isdir(images_directory) and not os.listdir(images_directory):
                os.rmdir(images_directory)
                
            return {"message": "Successfully deleted image"}, 200
        
        except OSError as e:
            return {"message": f"Failed to delete image: {str(e)}"}, 500


