from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ChemicalsReceived(models.Model):
    _name = "chemicals.received"
    _description = "Chemicals Received"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Name")
    item = fields.Char(string="item#")
    type = fields.Selection([('sds', 'SDS'), ('msds', 'MSDS'),('coa', 'COA'),('tds', 'TDS')],
                              string='Type')
    vendor_id = fields.Many2one('res.partner',string="Vendor")
    lot_code = fields.Char(string="Lot Code")
    related_file1 = fields.Binary(string="Related File1",attachment=True)
    related_file2 = fields.Binary(string="Related File (2)",attachment=True)
    related_image = fields.Binary(string="Related Image",attachment=True)
    product_id = fields.Many2one('product.template',string="Select Product")

