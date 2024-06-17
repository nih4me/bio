from django.contrib import admin

from import_export.formats import base_formats
from import_export.admin import ExportMixin as ExportMixinBase, ImportExportMixin as ImportExportMixinBase

from core.models import User, Page, CallToAction, OtherProfile, Keyword, CorporateType, Corporate, Experience, Education, SkillType, Skill, ServiceType, Service, PostType, Post
from core.resources import UserResource, CallToActionResource, PageResource, OtherProfileResource, KeywordResource, CorporateTypeResource, CorporateResource, ExperienceResource, EducationResource, SkillTypeResource, SkillResource, ServiceTypeResource, ServiceResource, PostTypeResource, PostResource

class ExportMixin(ExportMixinBase):
    def get_export_formats(self):
        formats = (
            base_formats.CSV,
        )
        return [f for f in formats if f().can_export()]
    
class ImportExportMixin(ImportExportMixinBase):
    def get_import_formats(self):
        formats = (
            base_formats.CSV,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.CSV,
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    resource_classes = [UserResource]
    list_display = ('first_name', 'last_name', 'email', 'username', 'phone', 'is_active')
    exclude = ('password', )
    list_filter = ('is_active', 'is_superuser', 'is_staff')
    filter_horizontal = ('groups', 'user_permissions')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    date_hierarchy = 'date_joined'
    
@admin.register(CallToAction)
class CallToActionAdmin(admin.ModelAdmin):
    resource_classes = [CallToActionResource]
    list_display = ('title', 'is_featured', 'user', 'is_active')
    list_filter = ('user', )
    filter_horizontal = ()
    search_fields = ('title', 'title')
    date_hierarchy = 'modified'

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    resource_classes = [PageResource]
    list_display = ('title', 'user', 'is_active')
    list_filter = ('user', )
    filter_horizontal = ()
    search_fields = ('context', 'title', 'description')
    date_hierarchy = 'modified'
    
@admin.register(OtherProfile)
class OtherProfileAdmin(admin.ModelAdmin):
    resource_classes = [OtherProfileResource]
    list_display = ('title', 'url', 'priority', 'user', 'is_active')
    list_filter = ('user', )
    filter_horizontal = ()
    search_fields = ('title', 'url')
    date_hierarchy = 'modified'

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    resource_classes = [KeywordResource]
    list_display = ('name', 'user', 'is_active')
    list_filter = ('user', )
    filter_horizontal = ()
    search_fields = ('name', )
    date_hierarchy = 'modified'
    
@admin.register(CorporateType)
class CorporateTypeAdmin(admin.ModelAdmin):
    resource_classes = [CorporateTypeResource]
    list_display = ('name', 'user', 'is_active')
    list_filter = ('user', )
    filter_horizontal = ()
    search_fields = ('name', )
    date_hierarchy = 'modified'
    
@admin.register(Corporate)
class CorporateAdmin(admin.ModelAdmin):
    resource_classes = [CorporateResource]
    list_display = ('name', 'corporate_type', 'user', 'is_active')
    list_filter = ('user', 'corporate_type')
    filter_horizontal = ()
    search_fields = ('name', )
    date_hierarchy = 'modified'
    
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    resource_classes = [ExperienceResource]
    list_display = ('position', 'employer', 'user', 'is_active')
    list_filter = ('user', )
    filter_horizontal = ('keywords', )
    search_fields = ('name', )
    date_hierarchy = 'modified'
    
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    resource_classes = [EducationResource]
    list_display = ('degree', 'course', 'user', 'is_active')
    list_filter = ('user', )
    filter_horizontal = ('hosts', )
    search_fields = ('name', )
    date_hierarchy = 'modified'
    
@admin.register(SkillType)
class SkillTypeAdmin(admin.ModelAdmin):
    resource_classes = [SkillTypeResource]
    list_display = ('name', 'priority', 'user', 'is_active')
    list_filter = ('user', )
    filter_horizontal = ()
    search_fields = ('name', )
    date_hierarchy = 'modified'
    
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    resource_classes = [SkillResource]
    list_display = ('name', 'level', 'skill_type', 'priority', 'user', 'is_active')
    list_filter = ('user', 'skill_type')
    filter_horizontal = ()
    search_fields = ('name', 'level')
    date_hierarchy = 'modified'
    
@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    resource_classes = [ServiceTypeResource]
    list_display = ('name', 'priority', 'user', 'is_active')
    list_filter = ('user', )
    filter_horizontal = ()
    search_fields = ('name', )
    date_hierarchy = 'modified'
    
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    resource_classes = [ServiceResource]
    list_display = ('title', 'user', 'is_active')
    list_filter = ('user', 'service_type')
    filter_horizontal = ('keywords', )
    search_fields = ('title', 'description')
    date_hierarchy = 'modified'
    
@admin.register(PostType)
class PostTypeAdmin(admin.ModelAdmin):
    resource_classes = [PostTypeResource]
    list_display = ('name', 'priority', 'user', 'is_active')
    list_filter = ('user', )
    filter_horizontal = ()
    search_fields = ('name', )
    date_hierarchy = 'modified'
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    resource_classes = [PostResource]
    list_display = ('title', 'user', 'is_active')
    list_filter = ('user', 'post_type')
    filter_horizontal = ('keywords', )
    search_fields = ('title', 'description')
    date_hierarchy = 'modified'