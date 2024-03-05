from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    volume = fields.Float(string="Volume")
