from django import forms
from .models import Birthday, Congratulation
from django.core.exceptions import ValidationError
# Импорт функции для отправки почты.
from django.core.mail import send_mail


BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}

# class BirthdayForm(forms.Form):
#    first_name = forms.CharField(max_length=20,
#                                 label='Имя')
#    last_name = forms.CharField(required=False,
#                                label='Фамилия',
#                                help_text='Необязательное поле')
#    birthday = forms.DateField(label='Дата рождения',
#                               widget=forms.DateInput(attrs={'type': 'date'}))
class CongratulationForm(forms.ModelForm):
    
    class Meta:
        model = Congratulation
        fields = ('text',)
        

class BirthdayForm(forms.ModelForm):
# Все настройки задаём в подклассе Meta.
    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Birthday
        # Указываем, что надо отобразить все поля.
        # fields = '__all__'
        # указываем какое поле исключить
        exclude = ('author',)
        # указать, что для поля с датой рождения 
        # используется виджет с типом данных
        widgets = {'birthday': forms.DateInput(attrs={'type': 'date'})
                   }
        
    def clean_first_name(self):
        # Получаем значение имени из словаря очищенных данных.
        first_name = self.cleaned_data['first_name']
        # Разбиваем полученную строку по пробелам 
        # и возвращаем только первое имя.
        return first_name.split()[0]
    
    def clean(self):
        # Вызов родительского метода clean.
        super().clean()
        # Получаем имя и фамилию из очищенных полей формы.
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        # Проверяем вхождение сочетания имени и фамилии во множество имён.
        if f'{first_name} {last_name}' in BEATLES:
            # Отправляем письмо, если кто-то представляется 
            # именем одного из участников Beatles.
            send_mail(
                subject='Another Beatles member',
                message=f'{first_name} {last_name} пытался опубликовать запись!',
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )
            raise ValidationError(
                'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
            ) 


class ContestForm(forms.Form):
    title = forms.CharField(max_length=20,
                            label='Название',
                            )
    description = forms.CharField(label='Описание',
                                 widget=forms.Textarea(attrs={'cols': '40', 'rows': '10'}))
    price = forms.IntegerField(label='Цена',
                               help_text='Рекомендованная розничная цена',
                               min_value=10,
                               max_value=100
                               )
    comment = forms.CharField(required=False,
                              label='Комментарий',
                              widget=forms.Textarea(attrs={'cols': '40', 'rows': '10'})
                              )