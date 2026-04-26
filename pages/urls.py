from django.urls import path

from pages.views import about_view, contact_view, faq_view, help_view, home_view

app_name = "pages"

urlpatterns = [
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    path("contact/", contact_view, name="contact"),
    path("help/", help_view, name="help"),
    path("faq/", faq_view, name="faq"),
]
