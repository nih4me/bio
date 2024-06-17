from django.views.generic import RedirectView, TemplateView
from django.http import Http404

from core.models import User, CallToAction, Page, Keyword, OtherProfile, Experience, Education, Skill, Service, Post
from research.models import ResearchTopic, Publication, Course

class RedirectToHome(RedirectView):
    permanent = False
    query_string = True
    pattern_name = "web:home_view"
    
class BaseTemplateView(TemplateView):
    def get_data(self):
        return dict()
    
    def dispatch(self, request, *args, **kwargs):
        user = None
        try:
            user_search_criteria = {
                'username': kwargs.get('user', ''),
                'is_active': True,
            }
            user = User.objects.filter(**user_search_criteria).values('username', 'grade', 'first_name', 'last_name', 'logo').first()
        except Exception as e:
            print(e)
        if user is None:
            request.session['profile'] = dict()
            raise Http404
        else:
            grade = user.get('grade')
            grade = '' if not grade else grade.strip()
            user['name'] = f"{user.get('last_name')} {user.get('first_name')}"
            user['initials'] = ''.join([l[0] for l in user['name'].split()])
            if grade:
                user['name'] = f"{grade} {user['name']}"
            request.session['profile'] = user
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_search_criteria = {
            'username': self.request.session['profile'].get('username', ''),
            'is_active': True,
        }
        user = User.objects.filter(**user_search_criteria).only('id').first()
        page_search_criteria = {
            'user': user,
            'context': self.context, 
            'is_active': True,
        }
        page = Page.objects.filter(**page_search_criteria).first()
        if page:
            context.update({
                'page': page,
            })
        context.update({
            f'{self.context}_is_active': 'active',
        })
        context.update(self.get_data())
        return context
    
class HomeView(BaseTemplateView):
    template_name = "home.html"
    context = template_name.split('.')[0]
    
    def get_data(self):
        data = dict()
        user_search_criteria = {
            'username': self.request.session['profile'].get('username', ''),
            'is_active': True,
        }
        user_info = [
            'phone', 'email', 'bio', 'current_position',
        ]
        user = User.objects.filter(**user_search_criteria).only(*user_info).first()
        if user:
            search_by_user_criteria = {
                'user': user,
                'is_active': True,
            }
            featured_call_to_action = CallToAction.objects.filter(**search_by_user_criteria, is_featured=True).first()
            other_profiles = OtherProfile.objects.filter(**search_by_user_criteria)
            keywords = Keyword.objects.filter(**search_by_user_criteria)
            experiences = Experience.objects.filter(**search_by_user_criteria)
            educations = Education.objects.filter(**search_by_user_criteria)
            skills = Skill.objects.filter(**search_by_user_criteria)
            data.update({
                'hide_full_name_in_text_logo': True,
                'profile': user,
                'featured_call_to_action': featured_call_to_action,
                'other_profiles': other_profiles,
                'keywords': keywords,
                'experiences': experiences,
                'educations': educations,
                'skills': skills,
                'progress_backgrounds_list': [
                    'bg-danger', 'bg-warning', 'bg-secondary', 'bg-info', 'bg-primary',
                ],
            })
        return data

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response
    

class ResearchView(BaseTemplateView):
    template_name = "research.html"
    context = template_name.split('.')[0]
    
    def get_data(self):
        data = dict()
        user_search_criteria = {
            'username': self.request.session['profile'].get('username', ''),
            'is_active': True,
        }
        user = User.objects.filter(**user_search_criteria).only('id').first()
        if user:
            search_by_user_criteria = {
                'user': user,
                'is_active': True,
            }
            research_topics = ResearchTopic.objects.filter(**search_by_user_criteria)
            keywords =  list()
            for research_topic in research_topics:
                keywords.extend(research_topic.keywords.all())
            keywords = set(keywords)
            call_to_actions = CallToAction.objects.filter(**search_by_user_criteria, call_type='research')
            data.update({
                'research_topics': research_topics,
                'keywords': keywords,
                'call_to_actions': call_to_actions,
            })
        return data
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response
    

class PublicationsView(BaseTemplateView):
    template_name = "publications.html"
    context = template_name.split('.')[0]
    
    def get_data(self):
        data = dict()
        user_search_criteria = {
            'username': self.request.session['profile'].get('username', ''),
            'is_active': True,
        }
        user = User.objects.filter(**user_search_criteria).only('id').first()
        if user:
            search_by_user_criteria = {
                'user': user,
                'is_active': True,
            }
            publications = Publication.objects.filter(**search_by_user_criteria)
            data.update({
                'publications': publications,
            })
        return data
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response
    
    
class TeachingView(BaseTemplateView):
    template_name = "teaching.html"
    context = template_name.split('.')[0]
    
    def get_data(self):
        data = dict()
        user_search_criteria = {
            'username': self.request.session['profile'].get('username', ''),
            'is_active': True,
        }
        user = User.objects.filter(**user_search_criteria).only('id').first()
        if user:
            search_by_user_criteria = {
                'user': user,
                'is_active': True,
            }
            courses = Course.objects.filter(**search_by_user_criteria)
            data.update({
                'courses': courses,
            })
        return data
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response
    
class ServiceView(BaseTemplateView):
    template_name = "service.html"
    context = template_name.split('.')[0]
    
    def get_data(self):
        data = dict()
        user_search_criteria = {
            'username': self.request.session['profile'].get('username', ''),
            'is_active': True,
        }
        user = User.objects.filter(**user_search_criteria).only('id').first()
        if user:
            search_by_user_criteria = {
                'user': user,
                'is_active': True,
            }
            services = Service.objects.filter(**search_by_user_criteria)
            data.update({
                'services': services,
            })
        return data
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response


class BlogView(BaseTemplateView):
    template_name = "blog.html"
    context = template_name.split('.')[0]
    
    def get_data(self):
        data = dict()
        user_search_criteria = {
            'username': self.request.session['profile'].get('username', ''),
            'is_active': True,
        }
        user = User.objects.filter(**user_search_criteria).only('id').first()
        if user:
            search_by_user_criteria = {
                'user': user,
                'is_active': True,
            }
            posts = Post.objects.filter(**search_by_user_criteria)
            data.update({
                'posts': posts,
            })
        return data
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response
    
    
class PostView(BaseTemplateView):
    template_name = "post.html"
    context = template_name.split('.')[0]
    post_id = None
    
    def get_context_data(self, **kwargs):
        try:
            self.post_id = kwargs.get('post_id', None)
        except Exception as e:
            print(e)
            raise Http404
        context = super().get_context_data(**kwargs)
        context.update(self.get_data())
        return context
    
    def get_data(self):
        data = dict()
        user_search_criteria = {
            'username': self.request.session['profile'].get('username', ''),
            'is_active': True,
        }
        user = User.objects.filter(**user_search_criteria).only('id').first()
        if user:
            search_by_user_criteria = {
                'user': user,
                'is_active': True,
            }
            post = Post.objects.filter(**search_by_user_criteria, id=self.post_id).first()
            if not post:
                print(self.post_id, '*' * 10)
                raise Http404
            data.update({
                'post': post,
            })
        return data
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response
