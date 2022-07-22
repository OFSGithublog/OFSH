from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PalletsTraceability(models.Model):
    _name = "pallet.pallet"
    _description = "Pallet Pallet"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'id'

    name = fields.Char(string="Pallet")


class PalletsTraceability(models.Model):
    _name = "pallets.traceability"
    _description = "Pallets"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, copy=False,
                       default=lambda self: _('New'))
    manufacturing_order_id = fields.Many2one('mrp.production', readonly=True,
                                             string="MO", store=True)
    client_id = fields.Many2one('res.partner', string="Client",
                                related="manufacturing_order_id.client_id",
                                store=True)
    product_id = fields.Many2one('product.product', string="Product",
                                 related="manufacturing_order_id.product_id",
                                 store=True,required=True)
    sku_code = fields.Char(string="SKU", related='product_id.default_code',
                           store=True)
    client_ref = fields.Char(string='Client PO#',
                             related="manufacturing_order_id.client_ref",
                             readonly=True, store=True)
    qa_pack_out = fields.Selection([('pass', 'Pass'), ('fail', 'Fail')],
                                   string="Q.A(Pack-out)", required=True)
    pallet_height = fields.Integer(string="Pallet Height")
    pallet_weight = fields.Integer(string="Pallet Weight")
    full_boxes_ids = fields.One2many('full.box', 'pallet_id', string='Foods')
    signature = fields.Binary(string="Signature", required=True)
    initial = fields.Char(string="Print Name")
    master_shipper_img = fields.Binary(attachment=True,
                                       string="Master Shipper Sticker Image")
    pallet_1 = fields.Binary(attachment=True, string="Pallet Image 1")
    pallet_2 = fields.Binary(attachment=True, string="Pallet Image 2")
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda self: self.env.company)
    comments = fields.Char(string='Comments')
    lot_code = fields.Char(string='Lot code',
                           related="manufacturing_order_id.lot_code",
                           store=True)
    product_qty = fields.Float(string='Ordered Quantity',
                               related="manufacturing_order_id.product_qty",
                               store=True)
    quantity_produced = fields.Float(string='Produced Quantity',
                                     related="manufacturing_order_id.quantity_produced",
                                     store=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'pallets.traceability') or 'New'
        res = super(PalletsTraceability, self).create(vals)
        return res

    @api.depends('full_boxes_ids')
    def _compute_total_boxes(self):
        if self.full_boxes_ids:
            self.total_boxes = False
            for rec in self.full_boxes_ids:
                self.total_boxes += rec.full_boxes
        else:
            self.total_boxes = False

    total_boxes = fields.Float(string="Total Boxes",
                               compute='_compute_total_boxes', store=True)

    @api.depends('full_boxes_ids')
    def _compute_total_qty(self):
        if self.full_boxes_ids:
            self.total_qty = False
            for rec in self.full_boxes_ids:
                self.total_qty += rec.subtotal
        else:
            self.total_qty = False

    total_qty = fields.Float(string="Total QTY", compute='_compute_total_qty',
                             store=True)
    qty = fields.Float(string='Quantity', required=True)

    @api.constrains('name')
    def _check_qty(self):
        if not self.env.context.get('pallets') == True:
            pass
        else:
            if not self.total_qty == self.qty:
                raise ValidationError(
                    _("Quantity error:Total qty should be '%s'", self.qty))
            mo_id = self.manufacturing_order_id
            if mo_id:
                bom_id = mo_id.bom_id
                if bom_id.type == 'normal' or bom_id.id == False:
                    new_production_qty = self.qty
                    if self.product_id.tracking == 'none':
                        vals = {'name': mo_id.name,
                             'product_id': self.product_id.id,
                             'product_uom': mo_id.product_uom_id.id,
                             'product_uom_qty': new_production_qty,
                             'location_id': self.product_id.property_stock_production.id,
                             'location_dest_id': mo_id.location_dest_id.id,
                             'state': 'done',
                             'origin': mo_id.name,
                             'picking_type_id': mo_id.picking_type_id.id,
                             'warehouse_id': mo_id.location_dest_id.warehouse_id.id,
                             'reference': mo_id.name,
                             'production_id': mo_id.id,
                             }
                        group_id = self.env[
                            'procurement.group'].search(
                            [('name', '=', mo_id.name)])
                        if group_id:
                            vals['group_id'] = group_id.id
                        finished_stock = self.env['stock.move'].create(
                            vals
                            )
                        values = {
                            'move_id': finished_stock.id,
                            'product_id': self.product_id.id,
                            'product_uom_id': mo_id.product_uom_id.id,
                            'qty_done': new_production_qty,
                            'location_id': self.product_id.property_stock_production.id,
                            'location_dest_id': mo_id.location_dest_id.id,
                            'state': 'done',
                            'reference': mo_id.name,
                            'production_id': mo_id.id
                        }
                        self.env['stock.move.line'].create(values)
                        if mo_id.order_id:
                            mo_picking_id = self.env[
                                'stock.picking'].search(
                                [('sale_id', '=', mo_id.order_id.id),
                                 ('backorder_id', '=', False),
                                 ('state', '!=', 'cancel')])
                            procurement = self.env[
                                'procurement.group'].search(
                                [('sale_id', '=', mo_id.order_id.id)])
                            sale_line_id = mo_id.order_id.order_line.filtered(
                                lambda r: r.product_id == mo_id.product_id)
                            mo_new_picking = self.env[
                                'stock.picking'].with_context(
                                {'manufacture_limit_picking': True}).create(
                                {'origin': mo_id.order_id.name,
                                 'move_type': mo_id.order_id.picking_policy,
                                 'group_id': procurement.id,
                                 'location_id': mo_picking_id.location_id.id,
                                 'location_dest_id': mo_picking_id.location_dest_id.id,
                                 'sale_id': mo_id.order_id.id,
                                 'state': 'waiting',
                                 'picking_type_id': mo_picking_id.picking_type_id.id,
                                 'partner_id': mo_id.order_id.partner_id.id,
                                 'company_id': self.env.company.id,
                                 })
                            move_id = self.env['stock.move'].create({
                                'product_id': mo_id.product_id.id,
                                'product_uom': mo_id.product_uom_id.id,
                                'name': mo_id.product_id.name,
                                'product_uom_qty': finished_stock.product_uom_qty,
                                'location_id': mo_new_picking.location_id.id,
                                'location_dest_id': mo_new_picking.location_dest_id.id,
                                'state': 'waiting',
                                'origin': mo_id.order_id.name,
                                'picking_type_id': mo_picking_id.picking_type_id.id,
                                'warehouse_id': mo_id.location_dest_id.warehouse_id.id,
                                'group_id': procurement.id,
                                'picking_id': mo_new_picking.id,
                                'reference': mo_new_picking.name,
                                'sale_line_id': sale_line_id.id,
                                'procure_method': 'make_to_stock',
                                'created_production_id': mo_id.id
                            })
                            # self.env['stock.move.line'].create({
                            #     'move_id': move_id.id,
                            #     'picking_id': mo_new_picking.id,
                            #     'product_id': mo_id.product_id.id,
                            #     'product_uom_id': mo_id.product_uom_id.id,
                            #     'product_uom_qty': finished_stock.product_uom_qty,
                            #     'location_id': move_id.location_id.id,
                            #     'location_dest_id': move_id.location_dest_id.id,
                            #     'state': 'waiting',
                            #     'reference': mo_new_picking.name,
                            #     'production_id': mo_id.id
                            # })
                        raw_materials = {}
                        for rec in bom_id.bom_line_ids:
                            raw_materials[rec.product_id] = rec.product_qty
                        bom_product_ids = mo_id.bom_id.bom_line_ids.mapped(
                            'product_id')
                        move_ids = list(mo_id.move_raw_ids)
                        bom_lines = [x for x in move_ids if
                                     x.product_id.id in bom_product_ids.ids and x.state != 'done']
                        for i in bom_lines:
                            if i.product_id.tracking == 'none':
                                new_qty = (raw_materials.get(i.product_id)/bom_id.product_qty)*new_production_qty
                                c = self.env['stock.move'].create(
                                    {'name': mo_id.name,
                                     'product_id': i.product_id.id,
                                     'product_uom': i.product_uom.id,
                                     'product_uom_qty': new_qty,
                                     'location_id': mo_id.location_src_id.id,
                                     'location_dest_id': i.product_id.property_stock_production.id,
                                     'state': 'done',
                                     'origin': mo_id.name,
                                     'picking_type_id': mo_id.picking_type_id.id,
                                     'warehouse_id': mo_id.location_dest_id.warehouse_id.id,
                                     'reference': mo_id.name,
                                     'raw_material_production_id': mo_id.id})
                                d = self.env['stock.move.line'].create({
                                    'move_id': c.id,
                                    'product_id': i.product_id.id,
                                    'product_uom_id': i.product_uom.id,
                                    'qty_done': new_qty,
                                    'location_id': mo_id.location_src_id.id,
                                    'location_dest_id': i.product_id.property_stock_production.id,
                                    'state': 'done',
                                    'reference': mo_id.name,
                                })
                                move_raw_line = mo_id.move_raw_ids.filtered(lambda x:x.product_id==i.product_id and x.state != 'done')
                                if move_raw_line:
                                    done_moves = mo_id.move_raw_ids.filtered(
                                        lambda x:
                                        x.state == 'done' and x.product_id == i.product_id)
                                    qty_produced = mo_id.product_id.uom_id._compute_quantity(
                                        sum(done_moves.mapped('product_qty')),
                                        mo_id.product_uom_id)
                                    qty_to_add = move_raw_line.product_uom_qty-qty_produced
                                    if qty_to_add <=0:
                                        move_raw_line.write(
                                            {'product_uom_qty': 0})
                                    else:
                                        move_raw_line.write({'product_uom_qty': qty_to_add})
                            else:
                                print('lot not supported')
                                # Updation needed for the products having tracking enabled

                        done_moves = mo_id.move_finished_ids.filtered(lambda x:
                                                                      x.state == 'done' and x.product_id == mo_id.product_id)
                        qty_produced = mo_id.product_id.uom_id._compute_quantity(
                            sum(done_moves.mapped('product_qty')),
                            mo_id.product_uom_id)
                        mo_id.quantity_produced+=new_production_qty
                        if mo_id.product_qty < qty_produced:
                            mo_id.product_qty = qty_produced
                            bom_draft_lines = [x for x in move_ids if
                                         x.product_id.id in bom_product_ids.ids and x.state != 'done']




class FullBox(models.Model):
    _name = "full.box"
    _description = "Full Boxes"

    pallet_id = fields.Many2one('pallets.traceability')
    lot_code_full = fields.Char(string="Lot Code")
    full_boxes = fields.Integer(string="#Boxes")
    description = fields.Char(string="Description")
    qty = fields.Float(string="QTY")
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal",
                            store=True)

    @api.depends('full_boxes', 'qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = float(rec.full_boxes) * rec.qty
