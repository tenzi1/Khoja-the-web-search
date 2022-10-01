from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse
from registration.backends.simple.views import RegistrationView

from khoja import views

#overriding the success url to point to update profile view
class KhojaRegistrationView(RegistrationView):
    def get_success_url(self, user=None):
        return reverse('khoja:register_profile')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', KhojaRegistrationView.as_view(), name='registration_register'),
    path('accounts/', include('registration.backends.default.urls')),
    path('', views.index, name="index"),
    path('khoja/', include('khoja.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
