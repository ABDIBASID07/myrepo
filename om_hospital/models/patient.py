from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "HospitalPatients"

    name = fields.Char(string='Name', tracking=True)
    ref = fields.Char(string='Reference')
    date_of_birth = fields.Date(string="Date Of Birth")
    age = fields.Integer(string="Age", compute='_compute_age', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True, default='male')
    active = fields.Boolean(string='Active', default=True)
    total_amount = fields.Float(string='Total Amount')

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    image = fields.Image(string='image')
    tag_ids = fields.Many2many('patient.tag', string='tags')
    prescription = fields.Html(string='Prescription')

    medicine_ids = fields.One2many('hospital.patient.medicine', 'patient_id', string='medicine')
    appointment_count = fields.Integer(string="Appointment_count", compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="appointments")

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_('The entered date is not acceptable'))

    @api.model
    def create(self, vals):
        vals["ref"] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals["ref"] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    def compute_bill(self):
        print("Bill Computed")

    # def name_get(self):
    #     patient_list = []
    #     for record in self:
    #         name = record.ref + " " + record.name
    #         patient_list.append((record.id, name))
    #         return patient_list

    def name_get(self):
        return [(record.id, "[%s] %s" % (record.ref, record.name)) for record in self]


class HospitalMedicine(models.Model):
    _name = "hospital.patient.medicine"
    _description = "hospital patient medicine"

    product_id = fields.Many2one('product.product')
    price_unit = fields.Float(string='Price', related="product_id.list_price")
    qty = fields.Integer(string='Quantity')
    sub_total = fields.Float(string="Sub Total", compute='_compute_total', tracking=True)
    # total = fields.Float(string="Sub Total", compute='_total', tracking=True)
    patient_id = fields.Many2one('hospital.patient', string="patient")

    @api.depends('price_unit', 'qty')
    def _compute_total(self):
        for rec in self:
            if rec.price_unit and rec.qty:
                rec.sub_total = rec.price_unit * rec.qty
            else:
                rec.sub_total = 0
