from odoo import models,fields,api,_
from odoo.exceptions import ValidationError


class pur_ord(models.Model):
    _inherit = 'sale.order'
    @api.model
    def create(self,vals_list):
        res = super(pur_ord, self).create(vals_list)
        print('yes its working')
        return res



class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    patient_name = fields.Char(string='patient Name')

class ResPartner(models.Model):
    _inherit = 'res.partner'
    company_type = fields.Selection(selection_add=[('Individual','community')])




class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Patient Record'

    @api.multi
    def test_cron_job(self):
        print("Your appointment has been scheduled")

    @api.multi
    def name_get(self):
        res=[]
        for rec in self:
            res.append((rec.id,'%s - %s' % (rec.name_seq, rec.patient_name)))
        return res

    @api.onchange('doctor_name')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_name:
                rec.dr_gender = rec.doctor_name.gender

    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age <=5:
                raise ValidationError(_('The age should be greater than 5'))
    @api.multi
    def print_send(self):
        return self.env.ref('Hostpital_Reports.report_patient_card').report_action(self)



    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age:
                if rec.patient_age < 18:
                    rec.age_group = 'minor'
                else:
                    rec.age_group = 'major'





    def open_patient_appointment(self):
        return {
            'name':('Appointment'),
            'domain':[('patient_id','=',self.id)],
            'view_type' : 'form',
            'res_model' : 'hospital.appointment',
            'view_id' : False,
            'view_mode' : 'tree, form',
            'type': 'ir.actions.act_window',
        }
    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id','=',self.id)])
        self.appointment_count = count
    def action_send_card(self):
        template_id = self.env.ref('Hostpital_Reports.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    _rec_name = 'patient_name'
    gender=fields.Selection([
        ('male','Male'),
        ('fe_male','Female'),],string='Gender')

    age_group = fields.Selection([
        ('major','Major'),
        ('minor','Minor'),
    ],string='Age Group',compute='set_age_group')

    doctor_name = fields.Many2one('hospital.doctor',string='dr_name')
    email = fields.Char(string='Email')
    dr_gender = fields.Selection([
        ('male','Male'),
        ('fe_male','Female')
    ])
    patient_name = fields.Char(string='Name', required=True, track_visibility="always")
    patient_age = fields.Integer('Age',group_operator=False)
    appointment_count = fields.Integer(string='Appointment', compute= 'get_appointment_count')
    active = fields.Boolean('Active',default=True)
    notes = fields.Text(String = 'Notes')
    patient_age2 = fields.Float(string="Age2")
    image = fields.Binary(String = 'Image')
    name = fields.Char(String='Test')
    user_id=fields.Many2one('res.users', string='PRO')
    name_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,index=True, default=lambda self: _('New'))
    patient_name_upper = fields.Char(compute='uper_name', inverse='inverse_name')
    @api.depends('patient_name')
    def uper_name(self):
        for rec in self:
            rec.patient_name_upper = rec.patient_name.upper() if rec.patient_name else False
    def inverse_name(self):
        for rec in self:
            rec.patient_name = rec.patient_name_upper.lower() if rec.patient_name_upper else False
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result