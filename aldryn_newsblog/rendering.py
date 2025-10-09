from django.shortcuts import render


def render_article_content(request, obj):
    return render(request, "aldryn_newsblog/article_content_preview.html", {"article": obj})
