
from odoo import api, fields, models, _
from odoo.tools import date_utils
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import datetime

class QCWizard(models.TransientModel):
    _name = "qc.wizard"
    _description = "QC Wizard"

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    mo_id = fields.Many2one('mrp.production', string='MO Id')

    def action_print_report(self):
        date_from = self.date_from
        date_to = self.date_to
        if date_to:
            date_to = datetime.datetime(date_to.year,date_to.month, date_to.day, 0, 0)
        if date_from:
            date_from = datetime.datetime(date_from.year,date_from.month, date_from.day, 0, 0)
        records = self.env['quality.control'].search([('mo_id','=',self.mo_id.id)])
        if date_to:
            records.filtered(lambda r:r.create_date <= date_to)
        if date_from:
            records.filtered(lambda r: r.create_date >= date_from)
        if records:
            return self.env.ref(
                'organic_filling_solutions.action_quality_control_report') \
                .report_action(records)
        else:
            return True