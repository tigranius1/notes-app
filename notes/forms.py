from django import forms
from .models import Note, Tag


class NoteForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        label='Теги (через запятую)',
        widget=forms.TextInput(attrs={'placeholder': 'работа, учёба, идеи'}),
    )

    class Meta:
        model = Note
        fields = ['title', 'text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tags_input'].initial = ', '.join(
                t.name for t in self.instance.tags.all()
            )

    def save(self, commit=True):
        note = super().save(commit=commit)
        if commit:
            self._save_tags(note)
        return note

    def _save_tags(self, note):
        raw = self.cleaned_data.get('tags_input', '') or ''
        names = [n.strip() for n in raw.split(',') if n.strip()]
        tags = []
        for name in names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        note.tags.set(tags)