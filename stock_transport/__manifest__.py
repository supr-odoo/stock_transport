{
    "name": "stock_transport",
    "application": True,
    "depends": ["stock_picking_batch", "fleet"],
    "data": [
        "security/ir.model.access.csv",
        "views/fleet_category_views.xml",
        "views/stock_picking_batch_views.xml",
        "views/inventory_batch_views.xml",
    ],
    "installable": True,
}
