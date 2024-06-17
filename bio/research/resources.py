from import_export import resources
from import_export.admin import ExportMixin

from research.models import ResearchTopic, PublicationType, Venue, Author, Publication, Course

class ResearchTopicResource(resources.ModelResource):
    class Meta:
        model = ResearchTopic
        
class PublicationTypeResource(resources.ModelResource):
    class Meta:
        model = PublicationType
        
class VenueResource(resources.ModelResource):
    class Meta:
        model = Venue
        
class AuthorResource(resources.ModelResource):
    class Meta:
        model = Author
        
class PublicationResource(resources.ModelResource):
    class Meta:
        model = Publication

class CourseResource(resources.ModelResource):
    class Meta:
        model = Course