from django.contrib import admin
from .models import Post,Category,Comment,Vote
from mptt.admin import MPTTModelAdmin

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'slug')
    prepopulated_fields = {'slug':('title',),}
admin.site.register(Post,PostAdmin)

admin.site.register(Category)
admin.site.register(Comment,MPTTModelAdmin)
admin.site.register(Vote)
