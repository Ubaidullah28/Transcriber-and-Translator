# speech/forms.py
from django import forms

LANGUAGE_CHOICES = [
    ('orig', 'Same as Speech (Only Transcribe)'),
    ('en', 'English'),
    ('ur', 'Urdu'),
    ('ar', 'Arabic'),
    ('hi', 'Hindi'),
    ('fr', 'French'),
    ('de', 'German'),
    ('es', 'Spanish'),
    ('zh-cn', 'Chinese (Simplified)'),
]

TRANSLATE_LANGUAGE_CHOICES = [
    ('auto', 'Detect Language Automatically'),
    ('en', 'English'),
    ('ur', 'Urdu'),
    ('ar', 'Arabic'),
    ('hi', 'Hindi'),
    ('fr', 'French'),
    ('de', 'German'),
    ('es', 'Spanish'),
    ('zh-cn', 'Chinese (Simplified)'),
]

class TranscriptionForm(forms.Form):
    audio_file = forms.FileField(
        label='Upload audio file',
        help_text='Supported: .wav, .mp3, .m4a, .webm etc.'
    )
    target_language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        label='Output language'
    )

class TranslationForm(forms.Form):
    source_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        label='Text to translate'
    )
    source_language = forms.ChoiceField(
        choices=TRANSLATE_LANGUAGE_CHOICES,
        label='From language'
    )
    target_language = forms.ChoiceField(
        choices=[c for c in TRANSLATE_LANGUAGE_CHOICES if c[0] != 'auto'],
        label='To language'
    )
