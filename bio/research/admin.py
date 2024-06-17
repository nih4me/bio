from django.contrib import admin

from research.models import ResearchTopic, PublicationType, Venue, Author, Publication, Course
from research.resources import ResearchTopicResource, PublicationTypeResource, VenueResource, AuthorResource, PublicationResource, CourseResource

@admin.register(ResearchTopic)
class ResearchTopicAdmin(admin.ModelAdmin):
    resource_classes = [ResearchTopicResource]
    list_display = ('name', 'is_active')
    list_filter = ('user', )
    filter_horizontal = ('keywords', )
    search_fields = ('name', )
    date_hierarchy = 'modified'
    
@admin.register(PublicationType)
class PublicationTypeAdmin(admin.ModelAdmin):
    resource_classes = [PublicationTypeResource]
    list_display = ('name', 'priority', 'is_active')
    list_filter = ('user', )
    filter_horizontal = ()
    search_fields = ('name', )
    date_hierarchy = 'modified'
    
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    resource_classes = [VenueResource]
    list_display = ('name', 'short_name', 'website', 'is_active')
    list_filter = ('user', )
    filter_horizontal = ()
    search_fields = ('name', 'short_name', 'website')
    date_hierarchy = 'modified'
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    resource_classes = [AuthorResource]
    list_display = ('first_name', 'last_name', 'email', 'is_active')
    list_filter = ('user', )
    filter_horizontal = ()
    search_fields = ('first_name', 'last_name', 'email')
    date_hierarchy = 'modified'
    
@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    resource_classes = [PublicationResource]
    list_display = ('title', 'is_active')
    list_filter = ('user', 'publication_type')
    filter_horizontal = ('keywords', )
    search_fields = ('title', 'abstract', 'authors')
    date_hierarchy = 'modified'
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    resource_classes = [CourseResource]
    list_display = ('name', 'code', 'is_active')
    list_filter = ('user', )
    filter_horizontal = ('keywords', )
    search_fields = ('name', 'description', 'code', 'url')
    date_hierarchy = 'modified'