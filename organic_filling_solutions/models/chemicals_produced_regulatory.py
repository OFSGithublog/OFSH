from odoo import api, fields, models, _


class ChemicalsProduced(models.Model):
    _name = "chemicals.produced"
    _description = "Chemicals Produced"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Name")

    related_file = fields.Binary(string="Related File",attachment=True)

    related_image = fields.Binary(string="Related Image",attachment=True)
