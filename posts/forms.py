from django import forms
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from .models import Post, Tag


class PostForm(forms.ModelForm):
    """
    Форма для создания и редактирования записи (поста).
    """

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=_("Теги"),
    )

    images = forms.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"]),
            MaxValueValidator(10 * 1024 * 1024, message=_("Изображение не должно превышать 10 МБ.")),
        ],
        label=_("Изображение"),
    )

    class Meta:
        model = Post
        fields = ["title", "content", "is_paid", "youtube_link", "images", "tags"]
        labels = {
            "title": _("Заголовок"),
            "content": _("Содержание"),
            "is_paid": _("Платная запись"),
            "youtube_link": _("Ссылка на YouTube"),
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
            "youtube_link": forms.URLInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Опционально: если нужно, динамически загружать теги или что-то

    def clean_images(self):
        image = self.cleaned_data.get("images")
        if image and image.size > 10 * 1024 * 1024:
            raise forms.ValidationError(_("Изображение превышает лимит в 10 МБ."))
        return image
