from odoo import models,fields,api,_
import pytz

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Appointment'
    _order = 'appointment_date desc'

    _rec_name = 'name_seq'


    def _get_default_note(self):
        return "your appointment fixed"

    def test_recordset(self):
        for rec in self:
            partners = self.env['res.partner'].search([])
            print("Partner =",partners.mapped('email'))
            print(" Sorted partners...", partners.sorted(lambda o: o.write_date, reverse=True))
            print(" Filtered partners...", partners.filtered(lambda o: not o.customer))


    def action_notify(self):
        for rec in self:
            rec.doctor_name.user_id.notify_info('hello, yor are developer')

    name_seq = fields.Char(string='Appointment Id', required=True, copy=False, readonly=True,index=True, default=lambda self: _('New'))
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    # @api.model
    # def default_get(self,fields):
    #     res = super(HospitalAppointment, self).default_get(fields)
    #     print('test..........')
    #     res['patient_id'] = 4
    #     return res

    def action_done(self):
        for rec in self:
            rec.state = 'done'
    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain':{'order_id':[('partner_id','=',rec.partner_id.id)]}}

    def delete_line(self):
        for rec in self:
            print('Time in UTC',rec.appointment_datetime)
            # user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            # print("user_tz",user_tz)
            # date_today = pytz.utc.localize(rec.appointment_datetime).astimezone(user_tz)
            # print('this in local timezone',date_today)
            rec.appointment_lines=[(15,0,0)]

    @api.model
    def default_get(self, fields):
        res = super(HospitalAppointment, self).default_get(fields)
        res['patient_id']=13
        res['notes']='follow me'
        appointment_lines = []
        product_rec = self.env['product.product'].search([],limit=5)
        for pro in product_rec:
            line = (0, 0, {
                'product_id': pro.id,
                'product_qty': 1,
            })
            appointment_lines.append(line)
        res.update({
            'appointment_lines': appointment_lines,
            'patient_id': 13,
            'notes': 'Like and Subscribe our channel To Get Notified'
        })
        return res

    user_id=fields.Many2one('res.users', string='PRO')
    patient_id = fields.Many2one('hospital.patient', string='patient', required=True)
    doctor_name= fields.Many2one('hospital.doctor',string='doctor')
    patient_age = fields.Integer('Age',related='patient_id.patient_age')
    notes=fields.Text(String="Registration Note",default=_get_default_note)
    doctor_note=fields.Text(String="Dr_Note")
    pharmacy_note=fields.Text(String="Pr_Note")
    appointment_lines = fields.One2many('hospital.appointment.line','appointment_id',string='Appointment Lines')
    appointment_date= fields.Date(string='Date')
    appointment_date_end= fields.Date(string='Date2')
    appointment_datetime= fields.Datetime(string='DateTime')
    partner_id = fields.Many2one('res.partner', string="Customer")
    order_id = fields.Many2one('sale.order', string="Sale Order")
    amount = fields.Float(string="Total Amount")
    state  = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('done','Done'),
        ('cancel','Cancelled'),
    ],string ='status', readonly=True,default='draft')

    product_id = fields.Many2one('product.template', string="Product Template")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            if rec.product_id:
                lines = [(5, 0, 0)]
                # lines = []
                print("self.product_id", self.product_id.product_variant_ids)
                for line in self.product_id.product_variant_ids:
                    val = {
                        'product_id': line.id,
                        'product_qty': 15
                    }
                    lines.append((0, 0, val))
                rec.appointment_lines = lines



    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result
    def del_data(self):
        for rec in self:
            print("your data is deleted")
            rec.appointment_lines=[(5,0,0)]




class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment.line'
    _description = 'Appointment Line'

    product_id = fields.Many2one('product.product',string='product')
    product_qty = fields.Integer(string='Quality')
    appointment_id = fields.Many2one('hospital.appointment',string='Appointment Id')
    sequence = fields.Integer(string='Sequence')