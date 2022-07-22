from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from odoo.tools import float_compare, float_round, float_is_zero, \
    format_datetime


class ManufacturingOrganicSolutions(models.Model):
    _inherit = 'mrp.production'

    image_128 = fields.Image(related='product_id.image_1920', readonly=True)

    description_file = fields.Binary(attachment=True, string="File")
    description_note = fields.Text(string='Notes', translate=True)
    order_id = fields.Many2one('sale.order')
    client_id = fields.Many2one('res.partner', related='order_id.partner_id',
                                string='Client', store=True,
                                readonly=False)
    client_ref = fields.Char(string='Client PO#', related='order_id.client_po',
                             store=True, readonly=False)
    lot_code = fields.Char(string='Lot code')
    bulk_provided_by_client = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                               string='Bulk Provided By client')
    bulk_approved = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                     string='Is Bulk Approved ?')
    approval_pic = fields.Binary(attachment=True,
                                 string="Upload Pictures of samples for approvals(1)")
    approval_pic2 = fields.Binary(attachment=True,
                                  string="Upload Pictures of samples for approvals(2)")
    approval_pic3 = fields.Binary(attachment=True,
                                  string="Upload Pictures of samples for approvals(3)")
    approval_pic4 = fields.Binary(attachment=True,
                                  string="Upload Pictures of samples for approvals(4)")
    delivery_count_mo = fields.Integer(string='New Delivery Orders',
                                       compute='_compute_manufacture_sale')
    pallet_count = fields.Integer(string='pallet count',
                                  compute='_compute_pallet')
    product_instructions_id = fields.Binary(
        related='product_id.product_instructions_id', attachment=True,
        string="SKU Instructions")
    parent_selected = fields.Selection(related='product_id.parent_selected',
                                       store=True)

    quantity_produced = fields.Float(string="Quantity to be Produced",
                                     digits="Product Unit Of Measure",
                                     copy=False, readonly=True)
    intial_demand = fields.Float(string="Intial Demand", readonly=True)

    invoice_count = fields.Integer(string='Invoices',
                                   compute='_get_invoiced_mo')
    delivery_invoice = fields.Boolean()


    @api.depends('order_id','order_id.invoice_status')
    def _get_invoice_status_mo(self):
        """
        Compute the invoice status of a SO. Possible statuses:
        - no: if the SO is not in status 'sale' or 'done', we consider that there is nothing to
          invoice. This is also the default value if the conditions of no other status is met.
        - to invoice: if any SO line is 'to invoice', the whole SO is 'to invoice'
        - invoiced: if all SO lines are invoiced, the SO is invoiced.
        - upselling: if all SO lines are invoiced or upselling, the status is upselling.
        """
        if not self.order_id:
            self.invoice_status = 'no'
        else:
            self.invoice_status = self.order_id.invoice_status


    invoice_status = fields.Selection([
        ('upselling', 'Upselling Opportunity'),
        ('invoiced', 'Fully Invoiced'),
        ('to invoice', 'To Invoice'),
        ('no', 'Nothing to Invoice')
    ], string='Invoice Status', compute='_get_invoice_status_mo')

    @api.depends('order_id.order_line.invoice_lines')
    def _get_invoiced_mo(self):
        for rec in self:
            if rec.order_id:
                invoices = rec.order_id.order_line.invoice_lines.move_id.filtered(
                    lambda r: r.move_type in ('out_invoice', 'out_refund'))
                rec.invoice_count = len(invoices)
            else:
                rec.invoice_count = 0

        # The invoice_ids are obtained thanks to the invoice lines of the SO
        # lines, and we also search for possible refunds created directly from
        # existing invoices. This is necessary since such a refund is not
        # directly linked to the SO.

    def button_invoice_mo(self):
        payment = self.env['sale.advance.payment.inv'].with_context({
            'active_model': 'sale.order',
            'active_ids': [self.order_id.id],
            'active_id': self.order_id.id,
        }).create({
            'advance_payment_method': 'delivered'
        })
        payment.create_invoices()

    @api.model
    def create(self, values):
        print(values)
        values['intial_demand'] = values['product_qty']
        res = super(ManufacturingOrganicSolutions, self).create(values)
        return res

    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Attachments',
        help='Attachments are linked to a document through model/res_id and to the message '
             'through this field.')
    qc_ids = fields.One2many('quality.control', 'mo_id', string="qc")

    def action_qc_report(self):
        qc_form = self.env.ref('organic_filling_solutions.view_qc_wizard_form')
        return {
            'name': _('Report'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'qc.wizard',
            'views': [(qc_form.id, 'form')],
            'target': 'new',
            'context': dict(self.env.context,
                            default_mo_id=self.id)
        }

    def action_qc_all(self):
        if self.qc_ids:
            return self.env.ref(
                'organic_filling_solutions.action_quality_control_report') \
                .report_action(self.qc_ids)

    def button_produce(self):
        view = self.env.ref(
            'organic_filling_solutions.view_pallet_wizard')
        return {
            'name': _('Produce'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'pallet.wizard',
            'views': [(view.id, 'form')],
            'target': 'new',
            'context': dict(self.env.context,
                            default_mo_id=self.id)
        }

    def action_view_delivery_manufacture(self):
        if self.order_id:
            return {
                'name': 'Transfers',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'res_model': 'stock.picking',
                'domain': [('sale_id', '=', self.order_id.id)],
                'target': 'current'
            }

    def action_view_pallet(self):
        pallet_id = self.env['pallets.traceability'].search(
            [('manufacturing_order_id', '=', self.id)]).ids
        return {
            'name': 'Pallets',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'pallets.traceability',
            'domain': [('id', '=', pallet_id)],
            'target': 'current'
        }

    @api.depends('name')
    def _compute_pallet(self):
        for rec in self:
            p_id = self.env['pallets.traceability'].search(
                [('manufacturing_order_id', '=', self.id)]).ids
            if len(p_id) > 0:
                picking_count = self.env['pallets.traceability'].search_count(
                    [('manufacturing_order_id', '=', self.id)])
                rec.pallet_count = picking_count
            else:
                rec.pallet_count = 0

    @api.depends('order_id')
    def _compute_manufacture_sale(self):
        for rec in self:
            if rec.order_id:
                picking_count = self.env['stock.picking'].search_count(
                    [('sale_id', '=', rec.order_id.id)])
                rec.delivery_count_mo = picking_count
            else:
                rec.delivery_count_mo = 0

    def button_mark_done(self):
        if self.order_id:
            #invoice needed
            if self.pallet_count==0:
                print("ok lets try something")
                #just super the method and to create invoice based on invoice policy
                res = super(ManufacturingOrganicSolutions,
                            self).button_mark_done()
                self.quantity_produced = self.qty_producing
                #invoice
                if self.env.context.get(
                        'button_mark_done_production_ids') or self.env.context.get(
                    'default_mo_ids') or self.env.context.get(
                    'skip_immediate'):
                    pass
                else:
                    if self.product_id.invoice_policy == 'order':
                        if self.invoice_status == 'to invoice':
                            inv = self.env['sale.advance.payment.inv'].create(
                                {
                                    'advance_payment_method': 'delivered'}).create_invoices()
                    else:
                        print("delivered")
                        self.write({'delivery_invoice':True})
                return res
            else:
                #change state of MO and cancel default lines
                #Also update the SO delivered based on Pallets
                #TO invoice on the delivered
                done_moves = self.move_finished_ids.filtered(lambda x:
                                                             x.state == 'done' and x.product_id == self.product_id)
                qty_produced = self.product_id.uom_id._compute_quantity(
                    sum(done_moves.mapped('product_qty')),
                    self.product_uom_id)
                sale_order = self.order_id
                ordered_product_qty = sale_order.order_line.filtered(
                    lambda x: x.product_id == self.product_id).product_uom_qty
                line = sale_order.order_line.filtered(
                    lambda x: x.product_id == self.product_id)
                if ordered_product_qty < qty_produced:
                    #over_production case:
                    self.env['sale.order.line'].browse(line.id).with_context(
                        {'manufacture_limit': True}).write({
                        'product_uom_qty': qty_produced})
                elif ordered_product_qty > qty_produced:
                    #under-production case:
                    self.env['sale.order.line'].browse(line.id).with_context(
                        {'manufacture_limit': True}).write({
                        'product_uom_qty': qty_produced})
                if self.env.context.get(
                        'button_mark_done_production_ids') or self.env.context.get(
                    'default_mo_ids') or self.env.context.get(
                    'skip_immediate'):
                    pass
                else:
                    if self.product_id.invoice_policy == 'order':
                        if self.invoice_status == 'to invoice':
                            inv = self.env['sale.advance.payment.inv'].create(
                                {
                                    'advance_payment_method': 'delivered'}).create_invoices()
                    else:
                        print("delivered")
                        self.write({'delivery_invoice': True})
                self.state = 'done'
                a = self.move_raw_ids.filtered(lambda tx: tx.state != 'done')
                for rec in a:
                    rec.state = 'cancel'
                    for rec2 in rec.move_line_ids:
                        rec2.state = 'cancel'
        else:
            #no invoice needed
            if self.pallet_count==0:
                #normal MO order
                res = super(ManufacturingOrganicSolutions,
                            self).button_mark_done()
                self.quantity_produced = self.qty_producing
                return res
            else:
                #change state of MO and cancel the line
                self.state = 'done'
                a = self.move_raw_ids.filtered(lambda tx: tx.state != 'done')
                for rec in a:
                    rec.state = 'cancel'
                    for rec2 in rec.move_line_ids:
                        rec2.state = 'cancel'

    def action_view_invoices(self):
        if self.order_id:
            invoices = self.order_id.mapped('invoice_ids')
            action = self.env["ir.actions.actions"]._for_xml_id(
                "account.action_move_out_invoice_type")
            if len(invoices) > 1:
                action['domain'] = [('id', 'in', invoices.ids)]
            elif len(invoices) == 1:
                form_view = [
                    (self.env.ref('account.view_move_form').id, 'form')]
                if 'views' in action:
                    action['views'] = form_view + [(state, view) for state, view
                                                   in action['views'] if
                                                   view != 'form']
                else:
                    action['views'] = form_view
                action['res_id'] = invoices.id
            else:
                action = {'type': 'ir.actions.act_window_close'}

            context = {
                'default_move_type': 'out_invoice',
            }
            if len(self) == 1:
                context.update({
                    'default_partner_id': self.order_id.partner_id.id,
                    'default_partner_shipping_id': self.order_id.partner_shipping_id.id,
                    'default_invoice_payment_term_id': self.order_id.payment_term_id.id or self.partner_id.property_payment_term_id.id or
                                                       self.env[
                                                           'account.move'].default_get(
                                                           [
                                                               'invoice_payment_term_id']).get(
                                                           'invoice_payment_term_id'),
                    'default_invoice_origin': self.order_id.name,
                    'default_user_id': self.user_id.id,
                })
            action['context'] = context
            return action
