from odoo import api, fields, models, _


class QualityControl(models.Model):
    _name = "quality.control"
    _description = "Quality Control"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    mo_id = fields.Many2one('mrp.production', string="MO")
    product_id = fields.Many2one('product.product', string="Product",
                                 related='mo_id.product_id',
                                 store=True)
    sku_code = fields.Char(string="SKU", related='product_id.default_code',
                           store=True)
    density = fields.Float(string="Density")
    range = fields.Char(string="Range")
    qc_frequency = fields.Selection([
        ('15_min', '15 Minutes'),
        ('30_min', '30 Minutes'),
        ('1_hr', '1 Hour'),
    ])
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)

    product_uom_id = fields.Many2one('uom.uom', string='Unit/M')
    lot_code = fields.Char(string='Lot code')
    avg_fill = fields.Float(string="Average Fill")
    no_people = fields.Float(string="No. of People")
    no_checks = fields.Integer(string="No. of Checks")
    no_bottles = fields.Integer(string="No. of Bottles")
    oil_wasted = fields.Float(string="Oil Wasted(kg)")
    eos_remaining = fields.Float(string="EOS Remaining")
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Attachments')
    initial = fields.Char(string="Print Name")
    signature = fields.Binary(string="Signature")
    time_table_ids = fields.One2many('quality.time.table', 'qlty_id')
    pallet_verify = fields.Boolean(string="10 % of pallet has been verified")
    initial_selection = fields.Selection([
        ('hd', 'HD'),
        ('ra', 'RA'),
        ('jm', 'JM'),
        ('sh', 'SH'), ('ng', 'NG'),
        ('nr', 'NR'), ('lc', 'LC'),
        ('s2', 'S2'), ('pb', 'PB'),
        ('ms', 'MS'),
    ], string="Initial")

    @api.onchange('qc_frequency')
    def _onchange_qc_frequency(self):
        if self.qc_frequency:
            if self.qc_frequency == '15_min':
                time_interval = 0.25
            elif self.qc_frequency == '30_min':
                time_interval = 0.5
            else:
                time_interval = 1.0
            start = 7.0
            end = 12.0
            cur_user = self.env.user.id
            self.with_user(1).time_table_ids = [(5, 0)]
            self.with_user(cur_user)
            while start <= end:
                self.write(
                    {
                        'time_table_ids': [(0, 0, {
                            'time': start
                        })]
                    }
                )
                start += time_interval

    def action_print_report(self):
        return self.env.ref(
            'organic_filling_solutions.action_quality_control_report') \
            .report_action(self)


class QualityControlTimeTable(models.Model):
    _name = "quality.time.table"
    _description = "Time Table"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    time = fields.Float(string='Time')
    p1 = fields.Char(string="P1")
    p2 = fields.Char(string="P2")
    vac = fields.Selection([('pass', 'Pass'), ('fail', 'Fail'), ('dt', 'DT')],
                           string='Vac.')
    pack = fields.Selection([('pass', 'Pass'), ('fail', 'Fail'), ('dt', 'DT')],
                            string='Pack')
    qlty_id = fields.Many2one('quality.control')
