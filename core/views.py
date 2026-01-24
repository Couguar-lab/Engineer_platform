from django.shortcuts import render

def contacts(request):
    """
    Отображает страницу контактов.
    """
    context = {
        'title': 'Контакты',
        'email': 'support@engineer-platform.ru', # пока пример
        'telegram': '@Cuguar',                   # пока пример
        # добавь телефон, форму обратной связи и т.д.
    }
    return render(request, 'core/contacts.html', context)