from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from django.views.generic import RedirectView

def health(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("health/", health, name="health"),
    path("", RedirectView.as_view(pattern_name="polls:index", permanent=False)),
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
]
