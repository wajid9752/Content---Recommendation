from django.contrib import admin
from .models import Tag, Category, Content , CustomUser , Content_Attributes
from django.contrib.auth.admin import UserAdmin

class UserAccountAdmin(UserAdmin):
    list_display=('email','is_active')
    search_fields=('email',)
    readonly_fields=('id',)
    ordering = ('email',)  # Specify a valid field for ordering
    fieldsets=(
        ('Personal',
            {
                'fields':('email','first_name','last_name')
            }),
            ('Permissions', {'fields': (
            'groups','user_permissions',
            )}),
            )

admin.site.register(CustomUser , UserAccountAdmin) 

class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']

admin.site.register(Tag, TagAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']

admin.site.register(Category, CategoryAdmin)

class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'created_at', 'updated_at']

admin.site.register(Content, ContentAdmin)
admin.site.register(Content_Attributes)
