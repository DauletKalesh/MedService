import io
from django.http import FileResponse
from django.template.loader import get_template
import trml2pdf

from datetime import datetime

def create_pdf(user_data):
    medical_history = user_data.med_history.all()
    for i in medical_history:
       print(i.symptoms)
    first_name = user_data.user.first_name
    last_name = user_data.user.last_name
    email = user_data.user.email
    date = datetime.today().strftime("%d %b, %Y")


    data = {'first_name': first_name, 'last_name': last_name, 'email': email, 'date': date,
              'medical_history': medical_history,}
    
    template = get_template('./pdf_structure.rml')
    xmlstring = template.render(data)
    pdfstr = trml2pdf.parseString(xmlstring)
    return pdfstr
#     return FileResponse(pdfstr, as_attachment=True, filename='{}_{}_medical_history_{}.pdf'.format(first_name, last_name, datetime.today().strftime("%d %b, %Y")))