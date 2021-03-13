from odoo import models, fields


# class SaleOrderInherit(models.Model):
#     _inherit = 'hospital.patient'
#     doctor_name = fields.Many2one('hospital.doctor',string='Dr_name')

# class hospital_doctor_name(models.Model):
#     _name= 'hostpitaldr.Name'
#     _inherits = {'hospital.patient':'dr_name'}
#
#     dr_name = fields.Char(string="Name")


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    # _inherits = {'hospital.patient': 'related_patient_id'}
    _description = 'Doctor Record'
    _rec_name = 'dr_name'

    dr_name = fields.Char(string="Name", required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], string="Gender")
    dr_age = fields.Integer(String='Doctor Age')
    dr_type = fields.Selection([
        ('Bone','bone'),
        ('Eye','eye'),
        ('Brain','brain')
    ],string="Specialist")
    user_id = fields.Many2one('res.users', string='Related User')
    # patient_id = fields.Many2one('hospital.patient.patient_age', string='Related Patient')
    # related_patient_id = fields.Many2one('hospital.patient', string='Related Patient ID')


