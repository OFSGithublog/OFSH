from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import warnings


class ProductCustomer(models.Model):
    _inherit = 'product.template'

    customer_id = fields.Many2one('res.partner', string='Client')

    product_instructions_id = fields.Binary(attachment=True,
                                            string="SKU Instructions")
    product_instructions_ids = fields.Many2many(
        'ir.attachment',
        string='ins',
        help='Attachments are linked to a document through model / res_id and to the message '
             'through this field.')
    parent_parent = fields.Many2one('parent.parent')
    parent_selected = fields.Selection(
        [('blend', 'Blend'), ('finish', 'Finish Products'), ('other', 'Other')],
        store=True)
    chemicals_received_ids = fields.One2many('chemicals.received', 'product_id',
                                             string='Chemical Received')
    parent_attribute1 = fields.Many2one('product.parent.attributes')
    parent_attribute2 = fields.Many2one('product.parent.attributes')
    parent_attribute3 = fields.Many2one('product.parent.attributes')
    parent_attribute4 = fields.Many2one('product.parent.attributes')
    parent_attribute5 = fields.Many2one('product.parent.attributes')
    parent_attribute6 = fields.Many2one('product.parent.attributes')
    parent_type1 = fields.Char(readonly=True, default='Parent')
    attribute_type1 = fields.Many2one('product.parent.type', readonly=True)
    attribute_type2 = fields.Many2one('product.parent.type', readonly=True)
    attribute_type3 = fields.Many2one('product.parent.type', readonly=True)
    attribute_type4 = fields.Many2one('product.parent.type', readonly=True)
    attribute_type5 = fields.Many2one('product.parent.type', readonly=True)
    attribute_type6 = fields.Many2one('product.parent.type', readonly=True)


    @api.onchange('default_code')
    def _onchange_default_code(self):
        # Overrided the existing warning functin for default_code
        pass

    @api.onchange('parent_parent')
    def _onchange_parent_check(self):
        if self.parent_parent:
            if self.parent_parent.name.lower() == 'blend':
                # self.parent_selected = 'blend'
                self.write({'parent_selected': 'blend'})
            elif self.parent_parent.name.lower() == 'finish product':
                print('f')
                self.write({'parent_selected': 'finish'})
            else:
                self.write({'parent_selected': 'other'})

    @api.onchange('parent_parent')
    def _onchange_parent_parent_domain(self):
        print('loaded')
        if self.parent_parent:
            attrs = self.parent_parent.attribute_mapping_ids.mapped('id')
            if attrs:
                attrs_key = [1, 2, 3, 4, 5, 6]
                attrs_zip = zip(attrs_key, attrs)
                attrs_dict = dict(attrs_zip)
                attrs_dict_keys = {}
                if attrs_dict.get(1):
                    attr1 = self.env['parent.parent.mapping'].search(
                        [('id', '=', attrs_dict.get(1))]).product_attributes.ids
                    attrs_dict_keys[1] = attr1
                if attrs_dict.get(2):
                    attr2 = self.env['parent.parent.mapping'].search(
                        [('id', '=', attrs_dict.get(2))]).product_attributes.ids
                    attrs_dict_keys[2] = attr2
                if attrs_dict.get(3):
                    attr3 = self.env['parent.parent.mapping'].search(
                        [('id', '=', attrs_dict.get(3))]).product_attributes.ids
                    attrs_dict_keys[3] = attr3
                if attrs_dict.get(4):
                    attr4 = self.env['parent.parent.mapping'].search(
                        [('id', '=', attrs_dict.get(4))]).product_attributes.ids
                    attrs_dict_keys[4] = attr4
                if attrs_dict.get(5):
                    attr5 = self.env['parent.parent.mapping'].search(
                        [('id', '=', attrs_dict.get(5))]).product_attributes.ids
                    attrs_dict_keys[5] = attr5
                if attrs_dict.get(6):
                    attr6 = self.env['parent.parent.mapping'].search(
                        [('id', '=', attrs_dict.get(6))]).product_attributes.ids
                    attrs_dict_keys[6] = attr6
                domain = {}
                if attrs_dict_keys.get(1):
                    domain['parent_attribute1'] = [
                        ('id', 'in',
                         attrs_dict_keys.get(1))]
                else:
                    domain['parent_attribute1'] = [
                        ('id', 'in',
                         [])]
                if attrs_dict_keys.get(2):
                    domain['parent_attribute2'] = [
                        ('id', 'in',
                         attrs_dict_keys.get(2))]
                else:
                    domain['parent_attribute2'] = [
                        ('id', 'in',
                         [])]
                if attrs_dict_keys.get(3):
                    domain['parent_attribute3'] = [
                        ('id', 'in',
                         attrs_dict_keys.get(3))]
                else:
                    domain['parent_attribute3'] = [
                        ('id', 'in',
                         [])]
                if attrs_dict_keys.get(4):
                    domain['parent_attribute4'] = [
                        ('id', 'in',
                         attrs_dict_keys.get(4))]
                else:
                    domain['parent_attribute4'] = [
                        ('id', 'in',
                         [])]
                if attrs_dict_keys.get(5):
                    domain['parent_attribute5'] = [
                        ('id', 'in',
                         attrs_dict_keys.get(5))]
                else:
                    domain['parent_attribute5'] = [
                        ('id', 'in',
                         [])]
                if attrs_dict_keys.get(6):
                    domain['parent_attribute6'] = [
                        ('id', 'in',
                         attrs_dict_keys.get(6))]
                else:
                    domain['parent_attribute6'] = [
                        ('id', 'in',
                         [])]
                if domain:
                    warnings.filterwarnings('ignore',r'^invalid escape sequence \'?\\.',category=DeprecationWarning)
                    return {'domain': domain}
            else:
                domain = {'parent_attribute1': [('id', 'in', [])],
                          'parent_attribute2': [('id', 'in', [])],
                          'parent_attribute3': [('id', 'in', [])],
                          'parent_attribute4': [('id', 'in', [])],
                          'parent_attribute5': [('id', 'in', [])],
                          'parent_attribute6': [('id', 'in', [])]}
                warnings.filterwarnings('ignore',r'^invalid escape sequence \'?\\.',category=DeprecationWarning)
                return {'domain': domain}

    @api.onchange('parent_parent')
    def _onchange_parent_parent(self):
        self.parent_attribute1 = False
        self.parent_attribute2 = False
        self.parent_attribute3 = False
        self.parent_attribute4 = False
        self.parent_attribute5 = False
        self.parent_attribute6 = False
        self.attribute_type1 = False
        self.attribute_type2 = False
        self.attribute_type3 = False
        self.attribute_type4 = False
        self.attribute_type5 = False
        self.attribute_type6 = False
        attrs_parent = self.parent_parent.attribute_mapping_ids.mapped(
            lambda r: r.product_type.id)
        attrs_pos = [1, 2, 3, 4, 5, 6]
        attrs_parent_dic = dict(zip(attrs_pos, attrs_parent))
        if attrs_parent_dic.get(1):
            self.attribute_type1 = attrs_parent_dic.get(1)
        if attrs_parent_dic.get(2):
            self.attribute_type2 = attrs_parent_dic.get(2)
        if attrs_parent_dic.get(3):
            self.attribute_type3 = attrs_parent_dic.get(3)
        if attrs_parent_dic.get(4):
            self.attribute_type4 = attrs_parent_dic.get(4)
        if attrs_parent_dic.get(5):
            self.attribute_type5 = attrs_parent_dic.get(5)
        if attrs_parent_dic.get(6):
            self.attribute_type6 = attrs_parent_dic.get(6)

    @api.constrains('default_code')
    def _check_default_code(self):
        for rec in self:
            if rec.default_code:
                if not rec.default_code == 'prda':
                    domain = [('default_code', '=', rec.default_code.lower())]
                    if rec.id:
                        domain.append(('id', '!=', rec.id))
                    if rec.env['product.template'].search(domain, limit=1):
                        raise ValidationError(
                            _('The Internal Reference (%s) already exists!',
                              rec.default_code))

    @api.constrains('name', 'parent_attribute1', 'parent_attribute2',
                    'parent_attribute3', 'parent_attribute4',
                    'parent_attribute5', 'parent_attribute6')
    def _edit_name(self):
        if self.parent_parent:
            parent_parent = self.parent_parent.id
            o2m = self.env['parent.parent'].browse(parent_parent)
            o2m_m2m = list(
                o2m.attribute_mapping_ids.mapped('product_attributes').ids)
            list_of = []
            parent_attribute1 = self.parent_attribute1.id
            parent_attribute2 = self.parent_attribute2.id
            parent_attribute3 = self.parent_attribute3.id
            parent_attribute4 = self.parent_attribute4.id
            parent_attribute5 = self.parent_attribute5.id
            parent_attribute6 = self.parent_attribute6.id
            list_of.extend(
                [parent_attribute1, parent_attribute2, parent_attribute3,
                 parent_attribute4, parent_attribute5, parent_attribute6])
            list_of_dict = dict(enumerate(list_of))

            for key, value in list_of_dict.items():
                if value != False:
                    if value in o2m_m2m:
                        pass
                    else:
                        a = self.env['parent.parent'].browse(
                            parent_parent).attribute_mapping_ids
                        b = a[key]
                        b.write({
                            'product_attributes': [(4, value)],
                        })

    @api.onchange('parent_parent', 'detailed_type')
    def _onchange_parent_set_route(self):
        if self.detailed_type != 'service':
            if self.parent_parent:
                if self.parent_parent.name.lower() == 'finish product':
                    mto = self.env.ref('stock.route_warehouse0_mto')
                    manufacture = self.env.ref(
                        'mrp.route_warehouse0_manufacture')
                    if mto.active == True and manufacture.active == True:
                        self.write(
                            {'route_ids': [(4, mto.id), (4, manufacture.id)]
                             })
                    buy = self.env.ref('purchase_stock.route_warehouse0_buy')
                    route_ids = self.route_ids.ids
                    if buy.id in route_ids:
                        self.write(
                            {'route_ids': [(3, buy.id)]
                             })

    @api.onchange('parent_parent', 'parent_attribute1', 'parent_attribute2',
                  'parent_attribute3', 'parent_attribute4', 'parent_attribute5',
                  'parent_attribute6')
    def _onchange_parent_parent_attes(self):
        code = []
        name = []
        if self.parent_parent:
            code.append(self.parent_parent.sequence)
            name.append(self.parent_parent.name)
        if self.parent_attribute1:
            code.append(self.parent_attribute1.code)
            name.append(self.parent_attribute1.name)
        if self.parent_attribute2:
            code.append(self.parent_attribute2.code)
            name.append(self.parent_attribute2.name)
        if self.parent_attribute3:
            code.append(self.parent_attribute3.code)
            name.append(self.parent_attribute3.name)
        if self.parent_attribute4:
            code.append(self.parent_attribute4.code)
            name.append(self.parent_attribute4.name)
        if self.parent_attribute5:
            code.append(self.parent_attribute5.code)
            name.append(self.parent_attribute5.name)
        if self.parent_attribute6:
            code.append(self.parent_attribute6.code)
            name.append(self.parent_attribute6.name)
        new_name = ",".join(name)
        new_code = "-".join(code)
        self.name = new_name
        self.default_code = new_code

    @api.model
    def create(self, vals):
        if vals.get('parent_parent'):
            parent_parent = vals.get('parent_parent')
            o2m = self.env['parent.parent'].browse(parent_parent)
            o2m_m2m = list(
                o2m.attribute_mapping_ids.mapped('product_attributes').ids)
            list_of = []
            parent_attribute1 = vals.get('parent_attribute1')
            parent_attribute2 = vals.get('parent_attribute2')
            parent_attribute3 = vals.get('parent_attribute3')
            parent_attribute4 = vals.get('parent_attribute4')
            parent_attribute5 = vals.get('parent_attribute5')
            parent_attribute6 = vals.get('parent_attribute6')
            list_of.extend(
                [parent_attribute1, parent_attribute2, parent_attribute3,
                 parent_attribute4, parent_attribute5, parent_attribute6])
            list_of_dict = dict(enumerate(list_of))
            for key, value in list_of_dict.items():
                if value != False:
                    if value in o2m_m2m:
                        pass
                    else:
                        a = self.env['parent.parent'].browse(
                            parent_parent).attribute_mapping_ids
                        b = a[key]
                        b.write({
                            'product_attributes': [(4, value)],
                        })

        res = super(ProductCustomer, self).create(vals)
        return res
