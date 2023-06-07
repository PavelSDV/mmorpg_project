# from django.forms import ModelForm, BooleanField # Импортируем true-false поле
from django.forms import ModelForm, BooleanField
from .models import Post

# Создаём модельную форму
class PostForm(ModelForm):
    check_box = BooleanField(label='Подтверждаю')  # добавляем галочку или же true-false поле
    class Meta:
        model = Post
        fields = ['title', 'categoryType', 'contentText', 'contentImage', 'contentFile', 'check_box']  # не забываем включить галочку в поля, иначе она не будет показываться на странице!

