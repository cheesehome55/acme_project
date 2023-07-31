from django.shortcuts import render
# Импортируем класс TemplateView, чтобы унаследоваться от него.
from django.views.generic import TemplateView
from birthday.models import Birthday


class HomePage(TemplateView):
    # В атрибуте template_name обязательно указывается имя шаблона,
    # на основе которого будет создана возвращаемая страница.
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста из родительского метода.
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь ключ total_count;
        # значение ключа — число объектов модели Birthday.
        context['total_count'] = Birthday.objects.count()
        # Возвращаем изменённый словарь контекста.
        return context


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию; 
    # выводить её в шаблон пользовательской страницы 404 мы не станем.
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403.html', status=403)