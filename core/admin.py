from django.contrib import admin
from project.settings.config import TEXT_TEMPLATES, PROJECT_SHORT_TITLE
from utils import dotdict

text = dotdict(TEXT_TEMPLATES.get('django_admin_panel'))

# Admin Dashboard Texts
admin.site.site_header = text.header.format(PROJECT_SHORT_TITLE)
admin.site.site_title = text.title.format(PROJECT_SHORT_TITLE)
admin.site.index_title = text.index_title.format(PROJECT_SHORT_TITLE)


