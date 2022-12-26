from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "HospitalAppointment"
    _rec_name = "patient_id"

    hide_sales_price = fields.Boolean(string='Hide Sales Price', default=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', ondelete='restrict')
    doctor_id = fields.Many2one('res.users', string="Doctor")
    gender = fields.Selection(string="Gender", related='patient_id.gender')
    appointment_time = fields.Datetime(string="Appointment Time", default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)
    # ref = fields.Char(string="Reference", related="patient_id.ref")
    ref = fields.Char(string="Reference")
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'normal'),
        ('1', 'low'),
        ('2', 'high'),
        ('3', 'very high')], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string="Stutus", default="draft", required=True, tracking=True)
    pharmacy_lines_ids = fields.One2many('appointment.pharmacy.line', 'appointment_id', string='Pharmacy Lines')

    #
    # @api.model
    # # def create(self, vals):
    # #     vals["name"] = self.env['ir.sequence'].next_by_code('hospital.appointment')
    # #     return super(HospitalAppointment, self).create(vals)
    # @api.model
    def hide_test(self):
        return

    # def unlink(self):
    #     if self.state != 'draft':
    #         raise ValidationError(_("You can only delete appointments only in draft states"))
    #     return super(HospitalAppointment, self).unlink()

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_test(self):
        print("Action Tested")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Congrts, You Successfully Clicked',
                'type': 'rainbow_man',
            }
        }

    def action_in_consultation(self):
        for rec in self:
            rec.state = "in_consultation"

    def action_done(self):
        for rec in self:
            rec.state = "done"

    def action_draft(self):
        for rec in self:
            rec.state = "draft"

    # def action_cancel(self):
    #     for rec in self:
    #         rec.state = "cancel"

    def action_cancel(self):
        action = self.env.ref('om_hospital.cancel_appointment_wizard').read()[0]
        return action


class AppointmentPharmacyLine(models.Model):
    _name = "appointment.pharmacy.line"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one('product.product')
    price_unit = fields.Float(string='Price', related="product_id.list_price")
    qty = fields.Integer(string='Quantity')
    appointment_id = fields.Many2one('hospital.appointment', string="appointment")
