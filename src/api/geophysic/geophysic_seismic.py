from flask_restx import Resource
from werkzeug.exceptions import NotFound
import os
import uuid

from src.api.nsmodels import geophysic_seismic_ns, geophysic_seismic_model, geophysical_seismic__parser
from src.models import GeophysicSeismic, Geophysical
from src.config import Config
from src.utils.utils import save_uploaded_file


@geophysic_seismic_ns.route('/geophysic_seismic/<int:geophy_id>')
class GeophysicSeismicAPI(Resource):
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
                os.path.join(Config.BASE_DIR, 'src', 'temp', str(proj_id), 'geophysical', str(geophy_id), 'archival_pdf'),
                ['application/pdf'],
                '.pdf'
            )
            if not pdf_filename:
                server_message += ' არ აიტვირთა PDF საარქივო ფაილი.'

        # Handle the Excel file upload
        if excel_files:
            excel_filename = save_uploaded_file(
                excel_files[0],
                os.path.join(Config.BASE_DIR, 'src', 'temp', str(proj_id), 'geophysical', str(geophy_id), 'archival_excel'),
                ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'],
                '.xlsx'
            )
            if not excel_filename:
                server_message += ' არ აიტვირთა Excel საარქივო ფაილი.'

        # Handle the Image file upload
        if img_files:
            img_filename = save_uploaded_file(
                img_files[0],
                os.path.join(Config.BASE_DIR, 'src', 'temp', str(proj_id), 'geophysical', str(geophy_id), 'archival_img'),
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