from django.contrib import admin
from django.urls import include, path, reverse_lazy
# Импортируем функцию, позволяющую серверу разработки отдавать файлы.
from django.conf.urls.static import static
# Импортируем настройки проекта.
from django.conf import settings
# Добавьте новые строчки с импортами классов.
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView


urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path(
        'auth/registration/', 
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('pages:homepage'),
        ),
        name='registration',
    ),
    # Подключаем urls.py приложения для работы с пользователями.
    path('auth/', include('django.contrib.auth.urls')),
    path('birthday/', include('birthday.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

# определяем вьюшку отвечающую за отрисовку 404
handler404 = 'pages.views.page_not_found'
# Если проект запущен в режиме разработки...
if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    # Подключаем функцию static() к urlpatterns: