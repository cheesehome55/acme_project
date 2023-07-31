from django.shortcuts import render, get_object_or_404, redirect
from .forms import BirthdayForm
from .models import Birthday
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown
# Импортируем класс пагинатора.
from django.core.paginator import Paginator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context 


class BirthdayMixin:
    model = Birthday
    # т.к. в модели указали get_absolute_url, сдесь можно убрать success_url
    # success_url = reverse_lazy('birthday:list')


class BirthdayFormMixin:
    form_class = BirthdayForm
    # страницу переименовали как имяПриложения_form, поэтому template_name не нужен
    # template_name = 'birthday/birthday.html'


class BirthdayCreateView(BirthdayMixin, BirthdayFormMixin, CreateView):
    pass


class BirthdayUpdateView(BirthdayMixin, BirthdayFormMixin, UpdateView):
    pass


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    pass 


class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10 
    

class BirthdayCreateView(CreateView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # Этот класс сам может создать форму на основе модели!
    # Нет необходимости отдельно создавать форму через ModelForm.
    # Указываем поля, которые должны быть в форме, ели не указан form_class:
    # fields = '__all__'
    # Указываем имя формы:
    form_class = BirthdayForm
    # Явным образом указываем шаблон:
    template_name = 'birthday/birthday.html'
    # Указываем namespace:name страницы, куда будет перенаправлен пользователь
    # после создания объекта:
    success_url = reverse_lazy('birthday:list') 


class BirthdayUpdateView(UpdateView):
    model = Birthday
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:list') 


# Создаём миксин.
class BirthdayMixin:
    model = Birthday
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:list')


# Добавляем миксин первым по списку родительских классов.
# class BirthdayCreateView(BirthdayMixin, CreateView):
    # Не нужно описывать атрибуты: все они унаследованы от BirthdayMixin.
    # pass


# class BirthdayUpdateView(BirthdayMixin, UpdateView):
    # И здесь все атрибуты наследуются от BirthdayMixin.
    # pass 


# Добавим опциональный параметр pk.
def birthday(request, pk=None):
    # Если в запросе указан pk (если получен запрос на редактирование объекта):
    if pk is not None:
        # Получаем объект модели или выбрасываем 404 ошибку.
        instance = get_object_or_404(Birthday, pk=pk)
    # Если в запросе не указан pk
    # (если получен запрос к странице создания записи):
    else:
        # Связывать форму с объектом не нужно, установим значение None.
        instance = None
    # Передаём в форму либо данные из запроса, либо None. 
    # В случае редактирования прикрепляем объект модели.
    form = BirthdayForm(request.POST or None,
                        # Файлы, переданные в запросе, указываются отдельно.
                        files=request.FILES or None,
                        instance=instance)
    # Остальной код без изменений.
    context = {'form': form}
    # Сохраняем данные, полученные из формы, и отправляем ответ:
    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context) 


class BirthdayDeleteView(DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list') 


def delete_birthday(request, pk):
    # Получаем объект модели или выбрасываем 404 ошибку.
    instance = get_object_or_404(Birthday, pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    # Если был получен POST-запрос...
    if request.method == 'POST':
        # ...удаляем объект:
        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect('birthday:list')
    # Если был получен GET-запрос — отображаем форму.
    return render(request, 'birthday/birthday.html', context)


def birthday2(request):
    # сли в GET-запросе были переданы параметры — значит, 
    # объект request.GET не пуст и этот объект передаётся в форму; 
    # если же объект request.GET пуст — срабатывает условиe or и форма 
    # создаётся без параметров,
    # через BirthdayForm(None) — это идентично обычному BirthdayForm()
    form = BirthdayForm(request.POST or None)
    context = {'form': form}
    # метод form.is_valid(): он возвращает True, если данные из запроса 
    # соответствуют ожидаемым типам в форме.
    if form.is_valid():
        # ...вызовем функцию подсчёта дней:
        birthday_countdown = calculate_birthday_countdown(
            # ...и передаём в неё дату из словаря cleaned_data.
            form.cleaned_data['birthday']
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        context.update({'birthday_countdown': birthday_countdown})
        form.save()
    
    return render(request, 'birthday/birthday.html', context=context)


def birthday_list(request):
    # Получаем список всех объектов с сортировкой по id.
    birthdays = Birthday.objects.order_by('id')
    # Создаём объект пагинатора с количеством 10 записей на страницу.
    paginator = Paginator(birthdays, 2)

    # Получаем из запроса значение параметра page.
    page_number = request.GET.get('page')
    # Получаем запрошенную страницу пагинатора. 
    # Если параметра page нет в запросе или его значение не приводится к числу,
    # вернётся первая страница.
    page_obj = paginator.get_page(page_number)
    # Вместо полного списка объектов передаём в контекст 
    # объект страницы пагинатора
    context = {'page_obj': page_obj}
    return render(request, 'birthday/birthday_list.html', context) 