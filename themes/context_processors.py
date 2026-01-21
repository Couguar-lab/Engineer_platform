from .models import Theme


def user_theme(request):
    """
    Контекст-процессор для передачи выбранной темы пользователя в шаблоны.
    Добавляет 'user_theme' в каждый шаблон.
    """
    if request.user.is_authenticated:
        theme = Theme.objects.filter(user=request.user).first()
        if not theme:
            # Создаём дефолтную тему при первом обращении
            theme = Theme.objects.create(user=request.user, theme="light")
        return {"user_theme": theme}
    return {"user_theme": None}
