from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class AppointmentController(http.Controller):
    @http.route('/Hostpital_Reports/appointments', auth='user', type='json')
    def appointment_banner(self):
        return {
            'html': """
                    <div>
                        <link>
                        <center><h1><font color="red">Subscribe the channel.......!</font></h1></center>
                        <center>
                        <p><font color="blue"><a href="https://www.youtube.com/channel/UCVKlUZP7HAhdQgs-9iTJklQ/videos">
                            Get Notified Regarding All The Odoo Updates!</a></p>
                            </font></div></center> """
        }




class WebsiteSaleInherit(WebsiteSale):
    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>''',
        '''/shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res = super(WebsiteSaleInherit, self).shop(self,page=0, category=None, search='', ppg=False, **post)
        print("Inherited Odoo Mates ....", res)
        return res


class Hospital(http.Controller):
    #sample controller created
    @http.route('/hospital/patient/',website=True, auth='user')
    def hospital_patient(self, **kw):
        patients = request.env['hospital.patient'].sudo().search([])
        # return "hello odoo mates"
        return request.render("Hostpital_Reports.products",{
            'patients': patients
        })

    class Hospital(http.Controller):
        @http.route('/patient_webform', type="http", auth="public", website=True)
        def patient_webform(self, **kw):
            print("Execution Here.........................")
            doctor_rec = request.env['hospital.doctor'].sudo().search([])
            print("doctor_rec...", doctor_rec)
            return http.request.render('Hostpital_Reports.create_patient', {'patient_name': 'Odoo Mates Test 123',
                                                                      'doctor_rec': doctor_rec})

        @http.route('/create/webpatient', type="http", auth="public", website=True)
        def create_webpatient(self, **kw):
            print("Data Received.....", kw)
            request.env['hospital.patient'].sudo().create(kw)
            # doctor_val = {
            #     'name': kw.get('patient_name')
            # }
            # request.env['hospital.doctor'].sudo().create(doctor_val)
            return request.render("Hostpital_Reports.patient_thanks", {})

