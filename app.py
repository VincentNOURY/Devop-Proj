from django.db import models
from django.http import HttpResponse
from django.views import View
from django.conf import settings
from django.core.wsgi import get_wsgi_application

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'users',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': 'mysql',
            'PORT': '3306',
        }
    },
    ROOT_URLCONF=__name__,
)

class User(models.Model):
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class HelloWorldView(View):
    def get(self, request):
        return HttpResponse('Hello, World!')

urlpatterns = [
    path('', HelloWorldView.as_view()),
]

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line([__file__, 'runserver'])