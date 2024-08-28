from flask_restx import Resource
from werkzeug.exceptions import NotFound
import os
import uuid

from src.api.nsmodels import geophysic_seismic_ns, geophysic_seismic_model, geophysical_seismic__parser
from src.models import GeophysicSeismic, Geophysical
from src.config import Config
from src.utils.utils import save_uploaded_file


@geophysic_seismic_ns.route('/geophysic_seismic/<int:geophy_id>')
class GeophysicSeismicListAPI(Resource):
    @geophysic_seismic_ns.marshal_with(geophysic_seismic_model)
    def get(self, geophy_id):
        geophysic_seismic = GeophysicSeismic.query.filter_by(geophysical_id=geophy_id).all()
        if not geophysic_seismic:
            raise NotFound("Geophysical not found")
        
        return geophysic_seismic, 200
    
    @geophysic_seismic_ns.doc(parser=geophysical_seismic__parser)
    def post(self, geophy_id):

        # Query the Geophysical model to get the proj_id
        geophysical_record = Geophysical.query.get(geophy_id)
        if not geophysical_record:
            raise NotFound("Geophysical record not found")

        proj_id = geophysical_record.project_id  # Get the project ID

        # Parse the incoming request data
        args = geophysical_seismic__parser.parse_args()

        # Extract files from the request
        pdf_files = args.get('archival_pdf', [])
        excel_files = args.get('archival_excel', [])
        img_files = args.get('archival_img', [])

        # Initialize filenames
        pdf_filename = None
        excel_filename = None
        img_filename = None
        server_message = "წარმატებით დაემატა სეისმური პროფილი."

        # Handle the PDF file upload
        if pdf_files:
            pdf_filename = save_uploaded_file(
                pdf_files[0],
                os.path.join(Config.BASE_DIR, 'src', 'temp', str(proj_id), 'geophysical', str(geophy_id), 'seismic', 'archival_pdf'),
                ['application/pdf'],
                '.pdf'
            )
            if not pdf_filename:
                server_message += ' არ აიტვირთა PDF საარქივო ფაილი.'

        # Handle the Excel file upload
        if excel_files:
            excel_filename = save_uploaded_file(
                excel_files[0],
                os.path.join(Config.BASE_DIR, 'src', 'temp', str(proj_id), 'geophysical', str(geophy_id), 'seismic', 'archival_excel'),
                ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'],
                '.xlsx'
            )
            if not excel_filename:
                server_message += ' არ აიტვირთა Excel საარქივო ფაილი.'

        # Handle the Image file upload
        if img_files:
            img_filename = save_uploaded_file(
                img_files[0],
                os.path.join(Config.BASE_DIR, 'src', 'temp', str(proj_id), 'geophysical', str(geophy_id), 'seismic', 'archival_img'),
                ['image/jpeg', 'image/png', 'image/jpg', 'image/gif']
            )
            if not img_filename:
                server_message += ' არ აიტვირთა სურათის საარქივო ფაილი.'

        # Create the Geophysical record
        new_geophysical_seismic = GeophysicSeismic(
            geophysical_id=geophy_id,
            longitude=args['longitude'],
            latitude=args['latitude'],
            profile_length=args['profile_length'],
            vs30=args['vs30'],
            ground_category_geo=args['ground_category_geo'],
            ground_category_euro=args['ground_category_euro'],
            archival_pdf=pdf_filename,
            archival_excel=excel_filename,
            archival_img=img_filename
        )
        new_geophysical_seismic.create()

        return {"message": server_message}, 200

@geophysic_seismic_ns.route('/geophysic_seismic/<int:geophy_id>/<int:id>')    
class GeophysicSeismicAPI(Resource):
    @geophysic_seismic_ns.marshal_with(geophysic_seismic_model)
    def get(self, geophy_id, id):
        geophysic_seismic = GeophysicSeismic.query.filter_by(geophysical_id=geophy_id, id=id).first()
        if not geophysic_seismic:
            raise NotFound("GeophysicSeismic not found")
        
        return geophysic_seismic, 200
    
    @geophysic_seismic_ns.doc(parser=geophysical_seismic__parser)
    def put(self, geophy_id, id):

        # Query the Geophysical model to get the proj_id
        geophysical_record = Geophysical.query.get(geophy_id)
        if not geophysical_record:
            raise NotFound("Geophysical record not found")

        proj_id = geophysical_record.project_id  # Get the project ID

        # Retrieve the record
        geophysic_seismic = GeophysicSeismic.query.filter_by(geophysical_id=geophy_id, id=id).first()
        if not geophysic_seismic:
            raise NotFound("Geophysical seismic record not found")

        # Parse the incoming request data
        args = geophysical_seismic__parser.parse_args()

        # Extract files from the request
        pdf_files = args.get('archival_pdf', [])
        excel_files = args.get('archival_excel', [])
        img_files = args.get('archival_img', [])

        # Initialize filenames
        pdf_filename = geophysic_seismic.archival_pdf
        excel_filename = geophysic_seismic.archival_excel
        img_filename = geophysic_seismic.archival_img
        server_message = "წარმატებით განახლდა სეისმური პროფილი."

        # Handle the PDF file upload
        if pdf_files:
            upload_folder = os.path.join(Config.BASE_DIR, 'src', 'temp', str(proj_id), 'geophysical', str(geophy_id), 'seismic', 'archival_pdf')
            pdf_filename = save_uploaded_file(
                pdf_files[0],
                upload_folder,
                ['application/pdf'],
                '.pdf'
            )
            if pdf_filename:
                # If there's an existing archival_pdf, delete it
                if geophysic_seismic.archival_pdf:
                    old_file_path = os.path.join(upload_folder, geophysic_seismic.archival_pdf)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)

                geophysic_seismic.archival_pdf = pdf_filename
            else:
                server_message += ' არ აიტვირთა PDF საარქივო ფაილი.'
            

        # Handle the Excel file upload
        if excel_files:
            upload_folder = os.path.join(Config.BASE_DIR, 'src', 'temp', str(proj_id), 'geophysical', str(geophy_id), 'seismic', 'archival_excel')
            excel_filename = save_uploaded_file(
                excel_files[0],
                upload_folder,
                ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'],
                '.xlsx'
            )
            if excel_filename:
                # If there's an existing archival_excel , delete it
                if geophysic_seismic.archival_excel:
                    old_file_path = os.path.join(upload_folder, geophysic_seismic.archival_excel)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)

                geophysic_seismic.archival_excel = excel_filename    
            else:
                server_message += ' არ აიტვირთა Excel საარქივო ფაილი.'

        # Handle the Image file upload
        if img_files:
            upload_folder = os.path.join(Config.BASE_DIR, 'src', 'temp',  str(proj_id), 'geophysical', str(geophy_id), 'seismic', 'archival_img')
            img_filename = save_uploaded_file(
                img_files[0],
                upload_folder,
                ['image/jpeg', 'image/png', 'image/jpg', 'image/gif']
            )
            if img_filename:
                # If there's an existing archival_img , delete it
                if geophysic_seismic.archival_img:
                    old_file_path = os.path.join(upload_folder, geophysic_seismic.archival_img)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                        
                geophysic_seismic.archival_img = img_filename
            else:    
                server_message += ' არ აიტვირთა სურათის საარქივო ფაილი.'

        # Update the record fields
        geophysic_seismic.longitude = args['longitude']
        geophysic_seismic.latitude = args['latitude']
        geophysic_seismic.profile_length = args['profile_length']
        geophysic_seismic.vs30 = args['vs30']
        geophysic_seismic.ground_category_geo = args['ground_category_geo']
        geophysic_seismic.ground_category_euro = args['ground_category_euro']

        # Save the updates
        geophysic_seismic.save()

        return {"message": server_message}, 200
    
    def delete(self, geophy_id, id):
        # Query the Geophysical model to get the proj_id
        geophysical_record = Geophysical.query.get(geophy_id)
        if not geophysical_record:
            raise NotFound("Geophysical record not found")

        proj_id = geophysical_record.project_id  # Get the project ID

        # Retrieve the Geophysic Seismic record
        geophysic_seismic = GeophysicSeismic.query.filter_by(geophysical_id=geophy_id, id=id).first()
        if not geophysic_seismic:
            raise NotFound("Geophysical seismic record not found")

        # Define paths for old files
        pdf_folder = os.path.join(Config.BASE_DIR, 'src', 'temp', str(proj_id), 'geophysical', str(geophy_id), 'seismic', 'archival_pdf')
        excel_folder = os.path.join(Config.BASE_DIR, 'src', 'temp', str(proj_id), 'geophysical', str(geophy_id), 'seismic', 'archival_excel')
        img_folder = os.path.join(Config.BASE_DIR, 'src', 'temp', str(proj_id), 'geophysical', str(geophy_id), 'seismic', 'archival_img')

        # Delete old files if they exist
        if geophysic_seismic.archival_pdf:
            old_pdf_path = os.path.join(pdf_folder, geophysic_seismic.archival_pdf)
            if os.path.exists(old_pdf_path):
                os.remove(old_pdf_path)
        
        if geophysic_seismic.archival_excel:
            old_excel_path = os.path.join(excel_folder, geophysic_seismic.archival_excel)
            if os.path.exists(old_excel_path):
                os.remove(old_excel_path)
        
        if geophysic_seismic.archival_img:
            old_img_path = os.path.join(img_folder, geophysic_seismic.archival_img)
            if os.path.exists(old_img_path):
                os.remove(old_img_path)

        # Delete the record from the database
        geophysic_seismic.delete()

        # Optionally remove empty directories
        for folder in [pdf_folder, excel_folder, img_folder]:
            if os.path.isdir(folder) and not os.listdir(folder):
                os.rmdir(folder)

        return {"message": "წარმატებით წაიშალა სეისმური პროფილი."}, 200