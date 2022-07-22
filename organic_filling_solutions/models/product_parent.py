from odoo import api, fields, models, _
from odoo.exceptions import ValidationError



class ProductParentType(models.Model):
    _name = "product.parent.type"
    _description = "Product type"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"

    name = fields.Char(string='Name', required=True)
    sequence_padding_no = fields.Integer(string='Sequence Padding',required=True)
    code_number = fields.Integer(default=1)
    attribute_ids = fields.One2many('product.parent.attributes','parent_type',string='Attributes values')


class ParentAttributes(models.Model):
    _name = "product.parent.attributes"
    _description = "Product Attributes"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"

    name = fields.Char(string='Name', required=True)
    parent_type = fields.Many2one('product.parent.type', string='Parent',
                                  required=True)
    code = fields.Char(string="code")

    @api.constrains('name')
    #CHECK UNIQUE NAMES
    def _check_name(self):
        name_ids = self.search([('parent_type','=',self.parent_type.id)]) - self
        value = [x.name.lower() for x in name_ids]
        if self.name and self.name.lower() in value:
            raise ValidationError(_('The name already Exists!'))
        return True

    def name_get(self):
        result = []
        for rec in self: result.append(
            (rec.id, '[%s] %s' % (rec.code, rec.name)))
        return result


    @api.model
    def create(self, values):
        pos = self.env.context.get('pos')
        o2m_id = self.env.context.get('on2m')
        if o2m_id:
            o2m = self.env['parent.parent'].browse(o2m_id)
            if o2m:
                parent = list(o2m.attribute_mapping_ids.mapped('product_type'))
                if len(parent)< pos-1:
                    pass
                else:
                    if pos:
                        parent_id = parent[pos-1].id
                        if parent_id:
                            values.update({'parent_type': parent_id})
        if values.get('parent_type'):
            parent = self.env['product.parent.type'].browse(
                values.get('parent_type'))
            padding = parent.sequence_padding_no
            code_number = parent.code_number
            values['code'] = str(code_number).zfill(padding)
            code_number += 1
            parent.write({'code_number': code_number})
            res = super(ParentAttributes, self).create(values)
            return res


class ParentParent(models.Model):
    _name = "parent.parent"
    _description = "Product Parent"
    _inherit = ['mail.thread', 'mail.activity.mixin']



    name = fields.Char(string='Name', required=True)
    sequence = fields.Char(string='Sequence', required=True, readonly=True,
                           copy=False,
                           default=lambda self: _('New'))
    attribute_mapping_ids = fields.One2many('parent.parent.mapping',
                                            'parent_id', string='Attributes')

    @api.constrains('attribute_mapping_ids')
    def _check_len(self):
        if len(self.attribute_mapping_ids) > 6:
            raise ValidationError(_("Limit exceeded!"))

    def name_get(self):
        result = []
        for rec in self: result.append(
            (rec.id, '[%s] %s' % (rec.sequence, rec.name)))
        return result

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'parent.parent') or 'New'
        return super(ParentParent, self).create(vals)


class ParentParentMapping(models.Model):
    _name = "parent.parent.mapping"
    _description = "Product Parent Mapping"
    _order = "sequence,id"

    sequence = fields.Integer(default=1)
    parent_id = fields.Many2one('parent.parent')
    product_type = fields.Many2one('product.parent.type',string="Parent Type")
    product_attributes = fields.Many2many('product.parent.attributes',string="Parent Attributes")


    @api.onchange('product_type','product_attributes')
    def _product_type(self):
        if self.product_type:
            attributes1 = self.product_type.attribute_ids.mapped("id")
            if attributes1:
                return {'domain': {'product_attributes': [
                    ('id', 'in',
                     attributes1)]}}
            else:
                return {'domain': {'product_attributes': [
                    ('id', 'in',
                     [])]}}


