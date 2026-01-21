from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Фильтр для получения значения из словаря по ключу.
    Использование: {{ prices|get_item:months }}
    """
    return dictionary.get(key, '0')