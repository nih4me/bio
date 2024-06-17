from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from django_jsonform.models.fields import JSONField
from django_countries.fields import CountryField
from tinymce.models import HTMLField

from datetime import date

from core.models import BaseModel, Corporate, Keyword

class ResearchTopic(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('name'))
    description = HTMLField(null=True, blank=True, verbose_name=_('description'))
    keywords = models.ManyToManyField(Keyword, blank=True, verbose_name=_('keywords'))
    image = models.FileField(upload_to ='uploads/topics', null=True, blank=True, verbose_name=_('image'))

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']
        verbose_name = _('topic')
        verbose_name_plural = _('topics')
        
class PublicationType(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    priority = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(1)], verbose_name=_('priority'))
    
    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']
        verbose_name = _('publication type')
        verbose_name_plural = _('publication types')
        
class Venue(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    short_name = models.CharField(max_length=25, verbose_name=_('short name'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    website = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('website'))
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        ordering = ['name']
        verbose_name = _('venue')
        verbose_name_plural = _('venues')

class Author(BaseModel):
    first_name = models.CharField(max_length=255, verbose_name=_('first name'),)
    last_name = models.CharField(max_length=255, verbose_name=_('last name'),)
    email = models.EmailField(null=True, blank=True, unique=True, verbose_name=_('email address'))

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = _('author')
        verbose_name_plural = _('authors')

class Publication(BaseModel):
    def _authors_schema():
        # TODO: Limit to current user
        _authors = Author.objects.all()
        choices = list()
        for _author in _authors:
            choices.append(
                {
                    'title': f'{_author.first_name} {_author.last_name}',
                    'value': str(_author.id),
                }
            )
        schema = {
            'type': 'array',
            'items': {
                'type': 'string',
                'choices': choices,
                'required': True,
            }
        }
        return schema
    
    publication_type = models.ForeignKey(PublicationType, on_delete=models.RESTRICT, verbose_name=_('publication type'))
    venue = models.ForeignKey(Venue, null=True, on_delete=models.RESTRICT, verbose_name=_('venue'))
    track = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('track'),)
    publication_date = models.DateField(null=True, blank=True, verbose_name=_('date'))
    title = models.TextField(verbose_name=_('title'))
    authors = JSONField(schema=_authors_schema)
    abstract = HTMLField(null=True, blank=True, verbose_name=_('abstract'))
    url = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('url'))
    note = HTMLField(null=True, blank=True, verbose_name=_('note'))
    keywords = models.ManyToManyField(Keyword, blank=True, verbose_name=_('keywords'))
    
    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['-created']
        verbose_name = _('publication')
        verbose_name_plural = _('publications')
        
class Course(BaseModel):
    def _teaching_periods_schema():
        # TODO: Limit to current user
        _corporates = Corporate.objects.all()
        corporates_choices = list()
        for _corporate in _corporates:
            corporates_choices.append(
                {
                    'title': f'{_corporate.name}',
                    'value': str(_corporate.id),
                }
            )
        schema = {
            'type': 'array',
            'items': {
                'type': 'dict',
                'keys': {
                    'institution': {
                        'type': 'string',
                        'title': _('Institution'),
                        'choices': corporates_choices,
                        'required': True,
                    },
                    'year': {
                        'type': 'number',
                        'title': _('Year'),
                        'minimum': 1970,
                        'maximum': date.today().strftime('%Y'),
                        'required': True,
                    },
                    'semester': {
                        'type': 'string',
                        'title': _('Semester'),
                        'choices': [_('Winter'), _('Summer')],
                        'required': True,
                    },
                }
            }
        }
        return schema
    
    name = models.TextField(verbose_name=_('name'))
    code = models.CharField(max_length=25, verbose_name=_('code'))
    teaching_periods = JSONField(schema=_teaching_periods_schema)
    keywords = models.ManyToManyField(Keyword, blank=True, verbose_name=_('keywords'))
    url = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('url'))
    image = models.FileField(upload_to ='uploads/topics', null=True, blank=True, verbose_name=_('image'))
    description = HTMLField(null=True, blank=True, verbose_name=_('description'))
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        ordering = ['name']
        verbose_name = _('course')
        verbose_name_plural = _('courses')