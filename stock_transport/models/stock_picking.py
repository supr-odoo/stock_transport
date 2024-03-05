from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    volume = fields.Float(string="Volume", compute="_compute_volume")

    @api.depends(
        "move_ids.product_id",
        "move_ids.quantity",
    )
    def _compute_volume(self):
        for record in self:
            total_volume = sum(
                move.product_id.volume * move.quantity for move in record.move_ids
            )
            record.volume = total_volume
