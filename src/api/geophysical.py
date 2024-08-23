from flask_restx import Resource
from werkzeug.exceptions import NotFound
import os
import uuid

from src.api.nsmodels import geophysical_ns, geophysical_model, geophysical_parser
from src.models import Geophysical
from src.config import Config


@geophysical_ns.route('/geophysical/<int:proj_id>')
@geophysical_ns.doc(responses={200: 'OK', 404: 'Geophysical not found'})
class GeophysicalListAPI(Resource):

    @geophysical_ns.marshal_with(geophysical_model)
    def get(self, proj_id):
        geophysical = Geophysical.query.filter_by(project_id=proj_id).all()
        if not geophysical:
            raise NotFound("Geophysical not found")
        
        return geophysical, 200
    
    @geophysical_ns.doc(parser=geophysical_parser)
    def post(self, proj_id):
        # Parse the incoming request data
        args = geophysical_parser.parse_args()

        # Extract the PDF file from the request
        pdf_files = args.get('archival_material', [])

        # Initialize file_path to None
        file_path = None

        # Handle the PDF file upload
        if pdf_files:
            # Check if there is at least one file
            if len(pdf_files) > 0:
                pdf_file = pdf_files[0]  # Get the first file in the list

                # Ensure the file is a PDF
                if pdf_file.mimetype == 'application/pdf':
                    # Generate a UUID4 and take the first 12 characters
                    filename = str(uuid.uuid4()).replace('-', '')[:12] + '.pdf'

                    # Define the directory to save the file
                    upload_folder = os.path.join(Config.BASE_DIR, 'src', 'temp', 'geophysical', 'archival_material', str(proj_id))
                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder)

                    # Construct the full file path
                    file_path = os.path.join(upload_folder, filename)

                    # Save the PDF file to the server
                    pdf_file.save(file_path)
                else:
                    return {'message': 'Only PDF files are allowed.'}, 400

        new_geophysical = Geophysical(
            project_id=proj_id,
            vs30=args['vs30'],
            ground_category_geo=args['ground_category_geo'],
            ground_category_euro=args['ground_category_euro'],
            archival_material=filename
        )
        new_geophysical.create()

        return {"message": "Successfully created project"}, 200

@geophysical_ns.route('/geophysical/<int:proj_id>/<int:id>')
@geophysical_ns.doc(responses={200: 'OK', 404: 'Geophysical not found'})
class GeophysicalAPI(Resource):
    @geophysical_ns.marshal_with(geophysical_model)
    def get(self, proj_id, id):
        # Query the Geophysical record with the specified project_id and id
        geophysical = Geophysical.query.filter_by(project_id=proj_id, id=id).first()
        if not geophysical:
            raise NotFound("Geophysical not found")
        
        return geophysical, 200
    
    @geophysical_ns.doc(parser=geophysical_parser)
    def put(self, proj_id, id):
        # Find the existing geophysical record
        geophysical = Geophysical.query.filter_by(project_id=proj_id, id=id).first()
        if not geophysical:
            raise NotFound("Geophysical not found")

        # Parse the incoming request data
        args = geophysical_parser.parse_args()

        # Extract the PDF file from the request
        pdf_files = args.get('archival_material', [])

        # Handle the PDF file upload
        if pdf_files:
            # Check if there is at least one file
            if len(pdf_files) > 0:
                pdf_file = pdf_files[0]  # Get the first file in the list

                # Ensure the file is a PDF
                if pdf_file.mimetype == 'application/pdf':
                    # Generate a UUID4 and take the first 12 characters
                    filename = str(uuid.uuid4()).replace('-', '')[:12] + '.pdf'

                    # Define the directory to save the file
                    upload_folder = os.path.join(Config.BASE_DIR, 'src', 'temp', 'geophysical', 'archival_material', str(proj_id))
                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder)

                    # Construct the full file path
                    file_path = os.path.join(upload_folder, filename)

                    # Save the PDF file to the server
                    pdf_file.save(file_path)

                    # Update the archival_material field with the new filename
                    geophysical.archival_material = filename
                else:
                    return {'message': 'Only PDF files are allowed.'}, 400

        # Update other fields
        geophysical.vs30 = args['vs30']
        geophysical.ground_category_geo = args['ground_category_geo']
        geophysical.ground_category_euro = args['ground_category_euro']

        # Save the changes
        geophysical.save()

        return {"message": "Successfully updated project"}, 200
    
    def delete(self, proj_id, id):
        # Fetch the geophysical record
        geophysical = Geophysical.query.filter_by(project_id=proj_id, id=id).first()
        if not geophysical:
            raise NotFound("Geophysical not found")

        # Delete the associated PDF file if it exists
        if geophysical.archival_material:
            upload_folder = os.path.join(Config.BASE_DIR, 'src', 'temp', 'geophysical', 'archival_material', str(proj_id))
            file_path = os.path.join(upload_folder, geophysical.archival_material)
            if os.path.exists(file_path):
                os.remove(file_path)

                # Optionally delete the directory if it's empty
                if not os.listdir(upload_folder):
                    os.rmdir(upload_folder)

        # Delete the geophysical record
        geophysical.delete()

        return {"message": "Successfully deleted geophysical record"}, 200