from django.shortcuts import render


def home_view(request):
    return render(request, "pages/home.html")


def about_view(request):
    return render(request, "pages/about.html")


def contact_view(request):
    return render(request, "pages/contact.html")


def help_view(request):
    return render(request, "pages/help.html")


def faq_view(request):
    return render(request, "pages/faq.html")
