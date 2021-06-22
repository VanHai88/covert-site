from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from taggit.models import Tag, TaggedItem

from .models import SiteData
from .models import Tag as MTag
class TagsModelAdmin(ModelAdmin):
    model = Tag
    menu_label = 'Tags' # ditch this to use verbose_name_plural from model
    menu_icon = 'tag' # change as required
    menu_order = 311 # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True # or True to add your model to the Settings sub-menu
    list_display = ["name", "slug"]
    #list_filter = ('live',)
    #search_fields = ('title',)

class MasterTagsModelAdmin(ModelAdmin):
    model = MTag
    menu_label = 'Master Tags' # ditch this to use verbose_name_plural from model
    menu_icon = 'tag' # change as required
    menu_order = 311 # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True # or True to add your model to the Settings sub-menu
    list_display = ["text", "slug", "parent"]

class SiteDataModelAdmin(ModelAdmin):
    model = SiteData
    menu_label = 'SiteData' # ditch this to use verbose_name_plural from model
    menu_icon = 'tag' # change as required
    menu_order = 311 # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True # or True to add your model to the Settings sub-menu
    list_display = ["key", "ftype"]

# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(TagsModelAdmin)
modeladmin_register(MasterTagsModelAdmin)
modeladmin_register(SiteDataModelAdmin)