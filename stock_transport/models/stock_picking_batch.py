from odoo import models, fields, api


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    dock_id = fields.Many2one("dock", string="Dock")
    vehicle_category_id = fields.Many2one(
        "fleet.vehicle.model.category", string="Vehicle Category"
    )
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle")

    volume = fields.Float(string="Volume", compute="_compute_volume", store=True)
    volume_graph = fields.Float(
        string="Volume Graph", compute="_compute_volume_graph", store=True
    )
    weight = fields.Float(string="Weight", compute="_compute_weight", store=True)
    weight_graph = fields.Float(
        string="Weight Graph", compute="_compute_weight_graph", store=True
    )
    transfers = fields.Integer(
        string="Transfers", compute="_compute_transfers", store=True
    )
    lines = fields.Integer(string="Lines", compute="_compute_lines", store=True)

    @api.depends("move_ids")
    def _compute_transfers(self):

        for record in self:
            record.transfers = len(record.picking_ids)

    @api.depends("picking_ids")
    def _compute_lines(self):
        for record in self:
            record.lines = len(record.move_ids)

    @api.depends("vehicle_category_id", "picking_ids", "picking_ids.volume")
    def _compute_volume_graph(self):
        for record in self:
            total_volume = sum(record.picking_ids.mapped("volume"))
            max_volume = record.vehicle_category_id.max_volume

            if max_volume:
                record.volume_graph = total_volume
            else:
                record.volume_graph = 0

    @api.depends("vehicle_category_id", "move_line_ids")
    def _compute_volume(self):
        for record in self:
            total_volume = sum(
                product.product_id.volume * product.quantity
                for product in record.move_line_ids
            )
            max_volume = (
                record.vehicle_category_id.max_volume
                if record.vehicle_category_id
                else 0
            )
            record.volume = (total_volume * 100) / max_volume if max_volume else 0

    @api.depends("vehicle_category_id", "move_line_ids")
    def _compute_weight(self):

        for record in self:
            total_weight = sum(
                product.product_id.weight * product.quantity
                for product in record.move_line_ids
            )
            max_weight = (
                record.vehicle_category_id.max_weight
                if record.vehicle_category_id
                else 0
            )
            record.weight = (total_weight * 100) / max_weight if max_weight else 0

    @api.depends("vehicle_category_id", "move_line_ids")
    def _compute_weight_graph(self):

        for record in self:
            total_weight = sum(
                product.product_id.weight * product.quantity
                for product in record.move_line_ids
            )
            record.weight_graph = total_weight

    def _compute_display_name(self):
        for record in self:
            product_volume = 0
            product_weight = 0
            for products in record.move_line_ids:
                product_volume += products.product_id.volume * products.quantity
                product_weight += products.product_id.weight * products.quantity
            record.display_name = (
                f"{record.name}: {product_weight} kg, {product_volume} m3"
            )
