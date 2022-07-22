from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"


    client_po = fields.Char(string='Client PO#')
