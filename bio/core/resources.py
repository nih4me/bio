from import_export import resources
from import_export.admin import ExportMixin

from core.models import User, CallToAction, Page, OtherProfile, Keyword, CorporateType, Corporate, Experience, Education, SkillType, Skill, ServiceType, Service, PostType, Post

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class CallToActionResource(resources.ModelResource):
    class Meta:
        model = CallToAction

class PageResource(resources.ModelResource):
    class Meta:
        model = Page
        
class OtherProfileResource(resources.ModelResource):
    class Meta:
        model = OtherProfile
        
class KeywordResource(resources.ModelResource):
    class Meta:
        model = Keyword

class CorporateTypeResource(resources.ModelResource):
    class Meta:
        model = CorporateType

class CorporateResource(resources.ModelResource):
    class Meta:
        model = Corporate
        
class ExperienceResource(resources.ModelResource):
    class Meta:
        model = Experience
        
class EducationResource(resources.ModelResource):
    class Meta:
        model = Education
        
class SkillTypeResource(resources.ModelResource):
    class Meta:
        model = SkillType
        
class SkillResource(resources.ModelResource):
    class Meta:
        model = Skill
        
class ServiceTypeResource(resources.ModelResource):
    class Meta:
        model = ServiceType
        
class ServiceResource(resources.ModelResource):
    class Meta:
        model = Service
        
class PostTypeResource(resources.ModelResource):
    class Meta:
        model = PostType
        
class PostResource(resources.ModelResource):
    class Meta:
        model = Post