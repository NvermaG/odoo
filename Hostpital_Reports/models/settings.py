from odoo import models,fields,api,_
from ast import literal_eval

class HospitalSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    note = fields.Char(string='Default Note')
    module_crm = fields.Boolean(string='CRM')
    product_ids = fields.Many2many('product.product', string='Medicines')


    def set_values(self):
        res = super(HospitalSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('Hostpital_Reports.note', self.note)
        self.env['ir.config_parameter'].set_param('Hostpital_Reports.product_ids', self.product_ids.ids)
        return res

    @api.model
    def get_values(self):
        res = super(HospitalSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        notes = ICPSudo.get_param('Hostpital_Reports.note')
        product_ids = self.env['ir.config_parameter'].sudo().get_param('Hostpital_Reports.product_ids')
        res.update(
                note=notes,
                product_ids=[(6, 0, literal_eval(product_ids))],
            )
        return res

