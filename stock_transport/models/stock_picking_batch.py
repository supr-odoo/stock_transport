from odoo import models, fields, api


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    dock_id = fields.Many2one("dock", string="Dock")
    vehicle_category_id = fields.Many2one(
        "fleet.vehicle.model.category", string="Vehicle Category"
    )
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle")

    volume = fields.Float(string="Volume", compute="_compute_volume")
    weight = fields.Float(string="Weight")
