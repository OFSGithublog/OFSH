from odoo import api, fields, models, _
from odoo.tools import date_utils
from odoo.exceptions import ValidationError


class PalletWizard(models.TransientModel):
    _name = "pallet.wizard"
    _description = "Pallet Wizard"

    mo_id = fields.Many2one('mrp.production', string='MO Id')
    company_id = fields.Many2one(
        'res.company', related='mo_id.company_id')
    quantity_produced = fields.Float(related='mo_id.quantity_produced')
    product_qty = fields.Float(related='mo_id.product_qty')
    product_id = fields.Many2one('product.product', related='mo_id.product_id',
                                 readonly=False, string='Product')
    qty = fields.Float(string='Quantity', required=True)

    def accept(self):
        print(self.product_qty,'ddddddddddddd')
        production_qty_available = self.product_qty - self.quantity_produced
        if self.qty > 0:
            view = self.env.ref(
                'organic_filling_solutions.view_pallets_traceability_form')
            return {
                'name': _('Pallet'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'pallets.traceability',
                'views': [(view.id, 'form')],
                'target': 'new',
                'context': dict({'pallets': True},
                                default_manufacturing_order_id=self.mo_id.id,
                                default_qty=self.qty),
            }

        else:
            raise ValidationError(
                _("Quantity Error: it should be above 0"))

