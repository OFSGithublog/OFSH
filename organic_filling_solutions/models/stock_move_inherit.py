from odoo import models,fields,_
from collections import defaultdict
from datetime import timedelta
from itertools import groupby
from odoo.tools import groupby as groupbyelem
from operator import itemgetter

from odoo import _, api, Command, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.tools.misc import clean_context, OrderedSet
class StockChatter(models.Model):
    _name = 'stock.move'
    _inherit = ['stock.move', 'mail.thread','mail.activity.mixin']

class StockButton(models.Model):
    _inherit = 'stock.move'

    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Attachments',
        help='Attachments are linked to a document through model / res_id and to the message '
             'through this field.',store=True,tracking=True)
    def button_attachements(self):
        print('self')





