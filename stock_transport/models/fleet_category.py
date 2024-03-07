from odoo import fields, models, api


class FleetVehicleModelCategory(models.Model):
    _inherit = "fleet.vehicle.model.category"
    _description = "Categories of fleet"

    max_weight = fields.Float(string="Max Weight (Kg)")
    max_volume = fields.Float(string="Max Volume (m³)")

    @api.depends("name", "max_weight", "max_volume")
    def _compute_display_name(self):
        for category in self:
            category.display_name = "%s (%.2f Kg, %.2f m³)" % (
                category.name,
                category.max_weight,
                category.max_volume,
            )
