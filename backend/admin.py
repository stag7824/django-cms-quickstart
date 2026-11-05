from cms.extensions import PageExtensionAdmin
from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Material, ResourceMeta


@admin.register(ResourceMeta)
class ResourceMetaAdmin(PageExtensionAdmin):
    pass


@admin.register(Material)
class MaterialAdmin(TranslatableAdmin):
    list_display = ["__str__", "technology", "category", "price_eur", "is_published", "position"]
    list_editable = ["is_published", "position"]
    list_filter = ["technology", "category", "is_published"]
