from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import SpecRow, SpecTable


@plugin_pool.register_plugin
class SpecTablePlugin(CMSPluginBase):
    model = SpecTable
    name = "Spec table"
    module = "Voxelry"
    render_template = "backend/plugins/spec_table.html"
    allow_children = True
    child_classes = ["SpecRowPlugin"]


@plugin_pool.register_plugin
class SpecRowPlugin(CMSPluginBase):
    model = SpecRow
    name = "Spec row"
    module = "Voxelry"
    render_template = "backend/plugins/spec_row.html"
    require_parent = True
    parent_classes = ["SpecTablePlugin"]
