from cms.extensions.toolbar import ExtensionToolbar
from cms.toolbar_pool import toolbar_pool
from django.utils.translation import gettext_lazy as _

from .models import ResourceMeta


@toolbar_pool.register
class ResourceMetaToolbar(ExtensionToolbar):
    model = ResourceMeta

    def populate(self):
        page_menu = self._setup_extension_toolbar()
        if page_menu:
            _extension, url = self.get_page_extension_admin()
            if url:
                page_menu.add_modal_item(
                    _("Resource settings"),
                    url=url,
                    disabled=not self.toolbar.edit_mode_active,
                )
