# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import odoo.addons.decimal_precision as dp

from odoo import fields, models, api


class purchase_custom_pricelist(models.Model):
    _name = "purchase.custom.pricelist"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name = "name"

    name = fields.Char(string="Tên hiển thị", index=True, copy=False, default="Mới")
    vendor_id = fields.Many2one(comodel_name="res.partner", string="Nhà cung cấp", required=True)
    product_id = fields.Many2one(comodel_name="product.product", string="Sản phẩm", required=True)
    product_qty = fields.Float(string="Số lượng", required=True)
    product_uom = fields.Many2one(comodel_name="product.uom", string="ĐVT", required=True)
    product_warranty = fields.Integer(string='Bảo Hành(tháng)', related="product_id.product_warranty")
    manufacturer = fields.Many2one(comodel_name="res.partner", string="Hãng sản xuất",
                                   related="product_id.manufacturer")
    product_country = fields.Many2one(comodel_name='res.country', string='Xuất xứ', ondelete='restrict',
                                      related="product_id.product_country")
    attribute_value_ids = fields.Many2many(comodel_name='product.attribute.value', string='Thông số kỹ thuật')
    price_unit = fields.Float(string='Giá', required=True, digits=dp.get_precision('Product Price'),
                              track_visibility="onchange")
    number_of_delivery_day = fields.Integer('Thời gian giao hàng(ngày)', track_visibility="onchange")
    start_date = fields.Date(string="Ngày báo giá", required=True, track_visibility="onchange")
    end_date = fields.Date(string="Ngày hết hiệu lực", track_visibility="onchange")

    # Work arround: force khi chọn tên nhà cung cấp tự get product attribute_value_ids
    @api.onchange("product_id", "vendor_id")
    def change_prod_attr(self):
        if self.product_id:
            self.attribute_value_ids = self.product_id.attribute_value_ids

    @api.model
    def create(self, vals):
        if vals.get('name', 'Mới') == 'Mới':
            vals['name'] = self.env["product.product"].browse(vals["product_id"]).display_name + "--" + self.env[
                "res.partner"].browse(vals["vendor_id"]).display_name or "Undefined"
        return super(purchase_custom_pricelist, self).create(vals)