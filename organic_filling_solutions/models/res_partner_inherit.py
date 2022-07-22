
from odoo import fields, models


class ResPartnerGroupBy(models.Model):
    _inherit = 'res.partner'

    contact_type = fields.Selection([
        ('client', 'Client'),
        ('vendor', 'Vendor')],string="Contact Type",default='client')