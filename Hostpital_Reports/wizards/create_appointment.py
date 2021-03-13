from odoo import models,fields,api,_


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    patient_name = fields.Many2one('hospital.patient', string ="patient")
    patient_id = fields.Many2one('hospital.patient', string ="patient")
    appointment_date = fields.Date(string="Appointment")
    # doctor_name = fields.Many2one('hospital.doctor',string='dr_name')

    def delete_patient(self):
        for rec in self:
            rec.patient_id.unlink()

    def create_appointment(self):
        vals={
            'patient_id': self.patient_id.id,
            'appointment_date':self.appointment_date,
            'notes':'hello this create by appoinment',
        }
        # self.env['hospital.appointment'].create(vals)
        self.patient_id.message_post(body='Appointment Created successfully', subject='Appointment')
        new_appointment = self.env['hospital.appointment'].create(vals)
        context = dict(self.env.context)
        context['form_view_initial_mode'] = 'edit'
        return {'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hospital.appointment',
                'res_id': new_appointment.id,
                'context': context
                }



    def get_data(self):
        appointments = self.env['hospital.appointment'].search([])
        print(appointments)
        # for rec in appointments:
        #     print(rec.patient_name)
        return {
            "type":"ir.actions.do_nothing"
        }

    @api.multi
    def print_report(self):
        data = {
            'model': 'create.appointment',
            'form': self.read()[0]
        }
        if data['form']['patient_id']:
            selected_patient = data['form']['patient_id'][0]
            appointments = self.env['hospital.appointment'].search([('patient_id', '=', selected_patient)])
        else:
            appointments = self.env['hospital.appointment'].search([])
        appointment_list = []
        for self in appointments:
            vals = {
                'name': self.name_seq,
                'notes': self.notes,
                'appointment_date': self.appointment_date
            }
            appointment_list.append(vals)
        # print("appointments", appointments)
        data['appointments'] = appointment_list
        # print("Data", data)
        return self.env.ref('Hostpital_Reports.appointment_report').with_context(landscape=True).report_action(self, data=data)



