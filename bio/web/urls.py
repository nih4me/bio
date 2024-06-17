from django.urls import path, include, re_path

from web.views import HomeView, ResearchView, PublicationsView, TeachingView, ServiceView, BlogView, PostView

app_name = "web"

urlpatterns = [
    path("<str:user>/", HomeView.as_view(), name="home_view"),
    path("<str:user>/research/", ResearchView.as_view(), name="research_view"),
    path("<str:user>/publications/", PublicationsView.as_view(), name="publications_view"),
    path("<str:user>/teaching/", TeachingView.as_view(), name="teaching_view"),
    path("<str:user>/service/", ServiceView.as_view(), name="service_view"),
    path("<str:user>/blog/", BlogView.as_view(), name="blog_view"),
    path("<str:user>/post/<uuid:post_id>", PostView.as_view(), name="post_view"),
]