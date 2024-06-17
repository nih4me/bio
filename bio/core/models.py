from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from django_jsonform.models.fields import JSONField
from django_countries.fields import CountryField
from tinymce.models import HTMLField

from core.managers import CustomUserManager

import uuid
        
class User(AbstractUser):
    first_name = models.CharField(_('first name'), blank=True, null=True, max_length=255)
    last_name = models.CharField(_('last name'), blank=True, null=True, max_length=255)
    username = models.CharField(_('username'), max_length=255, unique=True)
    grade = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('grade'))
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name=_('phone number'))
    logo = models.FileField(upload_to ='uploads/profile', null=True, blank=True, verbose_name=_('logo'))
    current_position = HTMLField(null=True, blank=True, verbose_name=_('current position'))
    bio = HTMLField(null=True, blank=True, verbose_name=_('bio'))
    street_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('street name'))
    street_number = models.IntegerField(null=True, blank=True, verbose_name=_('street number'))
    zip_code = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('zip code'))
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('city'))
    country = CountryField(null=True, blank=True, verbose_name=_('country'))

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

class BaseModel(TimeStampedModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name=_('id'))
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, verbose_name='Utilisateur')
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    
    class Meta:
        abstract = True
        
class Keyword(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('name'))

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']
        verbose_name = _('keyword')
        verbose_name_plural = _('keywords')

class CallToAction(BaseModel):
    CALL_TYPE = [
        ('research', 'Research'),
        ('other', 'Other')
    ]
    call_type = models.CharField(max_length=30, choices=CALL_TYPE, default='other', verbose_name=_('call type'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    content = HTMLField(null=True, blank=True, verbose_name=_('content'))
    is_featured = models.BooleanField(default=False, verbose_name=_('is featured'))
    
    class Meta:
        ordering = ['-created']
        verbose_name = _('call to action')
        verbose_name_plural = _('calls to action')
    
class Page(BaseModel):
    context = models.CharField(max_length=255, verbose_name=_('context'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    image = models.FileField(upload_to ='uploads/pages', null=True, blank=True, verbose_name=_('image'))

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['-created']
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        
class OtherProfile(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    url = models.CharField(max_length=255, verbose_name=_('url'))
    priority = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(1)], verbose_name=_('priority'))
    # TODO: Add iconify
    
    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['-created']
        verbose_name = _('other profile')
        verbose_name_plural = _('other profiles')

class CorporateType(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    
    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']
        verbose_name = _('corporate type')
        verbose_name_plural = _('corporate types')

class Corporate(BaseModel):
    corporate_type = models.ForeignKey(CorporateType, null=True, on_delete=models.RESTRICT, verbose_name=_('corporate type'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    short_name = models.CharField(max_length=25, null=True, blank=True, verbose_name=_('short name'))
    image = models.FileField(upload_to ='uploads/corporates', null=True, blank=True, verbose_name=_('image'))
    website = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('website'))
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('city'))
    country = CountryField(null=True, blank=True, verbose_name=_('country'))
    is_academia = models.BooleanField(default=False, verbose_name=_('is academia'))
    is_employer = models.BooleanField(default=False, verbose_name=_('is employer'))
    
    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-created']
        verbose_name = _('corporate')
        verbose_name_plural = _('corporates')
        
class Employer(Corporate):
    class ProxyEmployerManager(models.Manager):
        def get_queryset(self, *args, **kwargs):
            return super().get_queryset(*args, **kwargs).filter(is_employer=True)
    
    objects = ProxyEmployerManager()
    class Meta:
        proxy = True
        verbose_name = _('employer')
        verbose_name_plural = _('employers')
        
class Host(Corporate):
    class ProxyHostManager(models.Manager):
        def get_queryset(self, *args, **kwargs):
            return super().get_queryset(*args, **kwargs).filter(is_academia=True)
    
    objects = ProxyHostManager()
    class Meta:
        proxy = True
        verbose_name = _('host')
        verbose_name_plural = _('hosts')
        
class Experience(BaseModel):
    employer = models.ForeignKey(Employer, on_delete=models.RESTRICT, verbose_name=_('employer'))
    position = models.CharField(max_length=255, verbose_name=_('position'))
    job_description = HTMLField(null=True, blank=True, verbose_name=_('job description'))
    keywords = models.ManyToManyField(Keyword, blank=True, verbose_name=_('keywords'))
    start_date = models.DateField(verbose_name=_('start date'))
    end_date = models.DateField(null=True, blank=True, verbose_name=_('end date'))
    
    def __str__(self):
        return f'{self.position}'

    class Meta:
        ordering = ['-start_date']
        verbose_name = _('experience')
        verbose_name_plural = _('experiences')
        
class Education(BaseModel):
    hosts = models.ManyToManyField(Host, blank=True, verbose_name=_('hosts'))
    degree = models.CharField(max_length=255, verbose_name=_('degree'))
    course = models.CharField(max_length=255, verbose_name=_('course'))
    description = HTMLField(null=True, blank=True, verbose_name=_('description'))
    priority = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(1)], verbose_name=_('priority'))
    start_date = models.DateField(verbose_name=_('start date'))
    end_date = models.DateField(null=True, blank=True, verbose_name=_('end date'))
    
    def __str__(self):
        return f'{self.degree}'

    class Meta:
        ordering = ['priority']
        verbose_name = _('education')
        verbose_name_plural = _('educations')
        
class SkillType(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    priority = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(1)], verbose_name=_('priority'))
    
    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['priority']
        verbose_name = _('skill type')
        verbose_name_plural = _('skill types')
        
class Skill(BaseModel):
    skill_type = models.ForeignKey(SkillType, on_delete=models.RESTRICT, verbose_name=_('skill type'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = HTMLField(null=True, blank=True, verbose_name=_('description'))
    level = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)], verbose_name=_('level'))
    priority = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(1)], verbose_name=_('priority'))
    
    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['priority']
        verbose_name = _('skill')
        verbose_name_plural = _('skill')
        
class ServiceType(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    priority = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(1)], verbose_name=_('priority'))
    
    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['priority']
        verbose_name = _('service type')
        verbose_name_plural = _('service types')
        
class Service(BaseModel):
    def _occurrence_schema():
        schema = {
            'type': 'array',
            'items': {
                'type': 'dict',
                'keys': {
                    'start_date': {
                        'type': 'string',
                        'title': _('Start date'),
                        'format': 'date',
                        'required': True,
                    },
                    'end_date': {
                        'type': 'string',
                        'title': _('End date'),
                        'format': 'date',
                    },
                }
            }
        }
        return schema
    
    service_type = models.ForeignKey(ServiceType, on_delete=models.RESTRICT, verbose_name=_('service type'))
    title = models.TextField(verbose_name=_('title'))
    keywords = models.ManyToManyField(Keyword, blank=True, verbose_name=_('keywords'))
    beneficiary = models.CharField(max_length=255, verbose_name=_('beneficiary'))
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('city'))
    country = CountryField(null=True, blank=True, verbose_name=_('country'))
    description = HTMLField(null=True, blank=True, verbose_name=_('description'))
    occurrences = JSONField(null=True, blank=True, schema=_occurrence_schema)
    image = models.FileField(upload_to ='uploads/pages', null=True, blank=True, verbose_name=_('image'))
    url = models.CharField(null=True, blank=True, max_length=255, verbose_name=_('url'))
    
    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['-created']
        verbose_name = _('service')
        verbose_name_plural = _('services')
        
class PostType(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    priority = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(1)], verbose_name=_('priority'))
    
    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['priority']
        verbose_name = _('post type')
        verbose_name_plural = _('post types')
        
class Post(BaseModel):
    UI_TYPE = [
        ('default', 'Default'),
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('warning', 'Warning'),
        ('danger', 'Danger'),
    ]
    
    ui_type =   models.CharField(max_length=30, choices=UI_TYPE, default='default', verbose_name=_('ui type'))
    post_type = models.ForeignKey(PostType, on_delete=models.RESTRICT, verbose_name=_('post type'))
    title = models.TextField(verbose_name=_('title'))
    keywords = models.ManyToManyField(Keyword, blank=True, verbose_name=_('keywords'))
    content = HTMLField(verbose_name=_('content'))
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('city'))
    country = CountryField(null=True, blank=True, verbose_name=_('country'))
    image = models.FileField(upload_to ='uploads/pages', null=True, blank=True, verbose_name=_('image'))
    url = models.CharField(null=True, blank=True, max_length=255, verbose_name=_('url'))
    
    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['-created']
        verbose_name = _('post')
        verbose_name_plural = _('posts')