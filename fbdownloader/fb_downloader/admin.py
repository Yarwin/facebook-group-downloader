from django.contrib import admin

# Register your models here.
from .models import FbGroup, FbPost, FbUser, FbMedia

admin.site.register(FbGroup)
admin.site.register(FbPost)
admin.site.register(FbUser)
admin.site.register(FbMedia)