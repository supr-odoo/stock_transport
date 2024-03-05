from odoo import fields, models


class Dock(models.Model):
    _name = "dock"
    _description = "des"

    name = fields.Char(string="Dock")
