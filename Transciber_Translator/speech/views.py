# speech/views.py
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .forms import TranscriptionForm, TranslationForm
from .services.transcription import transcribe_audio_file
from .services.translation import translate_text


def home(request):
    return render(request, 'speech/home.html')


def transcribe_view(request):
    """
    Upload-based transcription.
    Optionally also translates transcript into user selected language.
    """
    transcript = None
    translated = None
    form = TranscriptionForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        audio = form.cleaned_data['audio_file']
        target_lang = form.cleaned_data['target_language']

        transcript = transcribe_audio_file(audio)

        if target_lang != 'orig':
            translated = translate_text(transcript, target_lang)
        else:
            translated = None

    context = {
        'form': form,
        'transcript': transcript,
        'translated': translated,
    }
    return render(request, 'speech/transcribe.html', context)


@csrf_exempt  # we manually send CSRF token in header from JS
def transcribe_record_view(request):
    """
    Live recording endpoint. Expects audio file in request.FILES['audio'].
    Returns JSON with transcript (and optional translation).
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("POST required")

    audio_file = request.FILES.get('audio')
    target_lang = request.POST.get('target_language', 'orig')

    if not audio_file:
        return HttpResponseBadRequest("No audio uploaded")

    transcript = transcribe_audio_file(audio_file)
    translated = None

    if target_lang != 'orig':
        translated = translate_text(transcript, target_lang)

    return JsonResponse({
        'transcript': transcript,
        'translated': translated,
    })


def translate_view(request):
    """
    Pure text translation page.
    """
    result = None
    form = TranslationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        text = form.cleaned_data['source_text']
        src = form.cleaned_data['source_language']
        dest = form.cleaned_data['target_language']

        result = translate_text(text, dest, src)

    return render(request, 'speech/translate.html', {
        'form': form,
        'result': result,
    })
