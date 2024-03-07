from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    volume = fields.Float(string="Volume", compute="_compute_volume", store=True)

    @api.depends("move_ids.product_id.volume", "move_ids.product_qty")
    def _compute_volume(self):
        for picking in self:
            total_volume = 0
            for move in picking.move_ids:
                if move.product_id and move.product_id.volume:
                    total_volume += move.product_id.volume * move.product_qty
            picking.volume = total_volume
