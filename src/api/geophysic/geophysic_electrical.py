from flask_restx import Resource
from werkzeug.exceptions import NotFound
import os

from src.api.nsmodels import geophysic_electrical_ns, geophysic_electrical_model, geophysic_electrical_parser
from src.models import GeophysicElectrical, Geophysical
from src.utils.utils import save_uploaded_file
from src.config import Config


@geophysic_electrical_ns.route('/geophysic_electrical/<int:geophy_id>')
class GeophysicElectricalListAPI(Resource):
    @geophysic_electrical_ns.marshal_with(geophysic_electrical_model)
    def get(self, geophy_id):
        geophysic_electrical = GeophysicElectrical.query.filter_by(geophysical_id=geophy_id).all()
        if not geophysic_electrical:
            raise NotFound("GeophysicElectrical not found")
        
        return geophysic_electrical, 200
    
    @geophysic_electrical_ns.doc(parser=geophysic_electrical_parser)
    def post(self, geophy_id):


        # Query the Geophysical model to get the proj_id
        geophysical_record = Geophysical.query.get(geophy_id)
        if not geophysical_record:
            raise NotFound("Geophysical record not found")

        proj_id = geophysical_record.project_id  # Get the project ID

        # Parse the incoming request data
        args = geophysic_electrical_parser.parse_args()

        # Extract files from the request
        pdf_files = args.get('archival_pdf', [])
        excel_files = args.get('archival_excel', [])
        img_files = args.get('archival_img', [])

        # Initialize filenames
        pdf_filename = None
        excel_filename = None
        img_filename = None
        server_message = "წარმატებით დაემატა ელექტრული პროფილი."

        # Handle the PDF file upload
        if pdf_files:
            pdf_filename = save_uploaded_file(
                pdf_files[0],
                os.path.join(Config.BASE_DIR, 'src', 'temp', str(proj_id), 'geophysical', str(geophy_id), 'electrical', 'archival_pdf'),
                ['application/pdf'],
                '.pdf'
            )
            if not pdf_filename:
                server_message += ' არ აიტვირთა საარქივო PDF-ის ფაილი.'

        # Handle the Excel file upload
        if excel_files:
            excel_filename = save_uploaded_file(
                excel_files[0],
                os.path.join(Config.BASE_DIR, 'src', 'temp', str(proj_id), 'geophysical', str(geophy_id), 'electrical', 'archival_excel'),
                ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'],
                '.xlsx'
            )
            if not excel_filename:
                server_message += ' არ აიტვირთა საარქივო Excel-ის ფაილი.'

        # Handle the Image file upload
        if img_files:
            img_filename = save_uploaded_file(
                img_files[0],
                os.path.join(Config.BASE_DIR, 'src', 'temp', str(proj_id), 'geophysical', str(geophy_id), 'electrical', 'archival_img'),
                ['image/jpeg', 'image/png', 'image/jpg', 'image/gif']
            )
            if not img_filename:
                server_message += ' არ აიტვირთა საარქივო Image-ის ფაილი.'


        # Create the GeophysicalSeismic record
        new_geophysical_electrical = GeophysicElectrical(
            geophysical_id=geophy_id,
            longitude=args['longitude'],
            latitude=args['latitude'],
            profile_length=args['profile_length'],
            archival_pdf=pdf_filename,
            archival_excel=excel_filename,
            archival_img=img_filename
        )
        new_geophysical_electrical.create()

        return {"message": server_message}, 200