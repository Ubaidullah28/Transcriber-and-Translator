// CSRF helper (reads cookie set by Django)
function getCookie(name) {
    let value = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                value = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return value;
}

const startBtn = document.getElementById('start-record-btn');
const stopBtn = document.getElementById('stop-record-btn');
const statusEl = document.getElementById('record-status');
const transcriptEl = document.getElementById('live-transcript');
const translatedEl = document.getElementById('live-translated');
const targetSelect = document.getElementById('record-target-language');

let mediaRecorder;
let audioChunks = [];

if (startBtn && stopBtn) {
    startBtn.addEventListener('click', async () => {
        transcriptEl.textContent = '';
        translatedEl.textContent = '';
        statusEl.textContent = 'Requesting microphone...';

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = e => {
                if (e.data.size > 0) audioChunks.push(e.data);
            };

            mediaRecorder.onstop = onRecordingStop;

            mediaRecorder.start();
            statusEl.textContent = 'Recording...';
            startBtn.disabled = true;
            stopBtn.disabled = false;
        } catch (err) {
            console.error(err);
            statusEl.textContent = 'Microphone access denied.';
        }
    });

    stopBtn.addEventListener('click', () => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            statusEl.textContent = 'Processing...';
            startBtn.disabled = false;
            stopBtn.disabled = true;
        }
    });
}

function onRecordingStop() {
    const blob = new Blob(audioChunks, { type: 'audio/webm' });
    const formData = new FormData();
    formData.append('audio', blob, 'recording.webm');
    formData.append('target_language', targetSelect.value);

    fetch('/transcribe/record/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            transcriptEl.textContent = data.transcript || '';
            translatedEl.textContent = data.translated || '';
            statusEl.textContent = 'Done.';
        })
        .catch(err => {
            console.error(err);
            statusEl.textContent = 'Error while transcribing.';
        });
}
