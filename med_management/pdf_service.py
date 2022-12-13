import jinja2
import pdfkit
from datetime import datetime
def create_pdf(user_data):
    medical_history = user_data.med_history.first()
    first_name = user_data.profile.user.first_name
    last_name = user_data.profile.user.last_name
    email = user_data.profile.user.email
    date = today_date = datetime.today().strftime("%d %b, %Y")
    date_of_record = 'frw'
    symptoms = 'dfdgdd'
    diagnosis = 'dslkdfjkldfjkl'

    context = {'first_name': first_name, 'last_name': last_name, 'email': email, 'date': date,
           'date_of_record': date_of_record, 'symptoms': symptoms, 'diagnosis':diagnosis}
    print(context)

    template_loader = jinja2.FileSystemLoader('./')
    print(template_loader)
    template_env = jinja2.Environment(loader=template_loader)
    print(template_env)

    html_template = 'basic-template.html'
    template = template_env.get_template(html_template)
    print(template)
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    output_pdf = 'pdf_generated.pdf'
    pdfkit.from_string(output_text, output_pdf, configuration=config, css='style.css')