const sessionForm = document.querySelector('#sessionForm');
const editSessionForm = document.querySelector('#editSessionForm');
const radios = document.querySelectorAll('input[name="subtitles"]');
const radiosEdited = document.querySelectorAll('input[name="subtitlesEdited"]');
let selectedRadio = '';
let selectedRadioEdited = '';

const calculateEndTime = (startTime, durationMinutes) => {
  const startDate = new Date(startTime);
  const endDate = new Date(startDate.getTime() + durationMinutes * 60000);

  const year = endDate.getFullYear();
  const month = String(endDate.getMonth() + 1).padStart(2, '0');
  const day = String(endDate.getDate()).padStart(2, '0');
  const hours = String(endDate.getHours()).padStart(2, '0');
  const minutes = String(endDate.getMinutes()).padStart(2, '0');

  return `${year}-${month}-${day} ${hours}:${minutes}`;
};

radios.forEach(radio => {
    radio.addEventListener('change', (e) => {
        selectedRadio = e.target.value;
    });
});

radiosEdited.forEach(radio => {
    radio.addEventListener('change', (e) => {
        selectedRadioEdited = e.target.value;
    });
});

const loadSessions = async () => {
    try {
        const response = await fetch('/session/all');
        const data = await response.json();
        const sessions = data.sessions;
        const sessionContainer = document.querySelector('#sessionList');
        sessionContainer.innerHTML = '';

        sessions.forEach(session => {
            console.log(session.start_time);
            const sessionCard = document.createElement('div');
            sessionCard.className = 'bg-stone-800 flex flex-col border-2 border-stone-700 rounded-lg p-4';

            sessionCard.innerHTML = `
                <div class="flex justify-between items-start mb-2">
                    <h3 class="text-orange-400 font-bold text-lg">Sessão #${session.id}</h3>
                     <div class="flex justify-between gap-2 p-2 mt-auto">
                    <button class="delete-btn text-red-100 hover:text-orange-400 cursor-pointer hover:scale-150 transition duration-300" 
                         data-id="${session.id}">🗑️</button>
                    <button class="edit-btn text-red-100 hover:text-orange-400 cursor-pointer hover:scale-150 transition duration-300" 
                         data-session='${JSON.stringify(session).replace(/'/g, "&#39;")}'>✏️</button>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-2 text-red-100">
                    <p><span class="text-orange-300">Filme:</span> #${session.movie_id}</p>
                    <p><span class="text-orange-300">Sala:</span> ${session.room_number}</p>
                    <p><span class="text-orange-300">Início:</span> ${new Date(session.start_time).toLocaleString()}</p>
                    <p><span class="text-orange-300">Término:</span> ${new Date(session.end_time).toLocaleString()}</p>
                    <p><span class="text-orange-300">Idioma:</span> ${session.language}</p>
                    <p><span class="text-orange-300">Legendas:</span> ${session.subtitles ? 'Sim' : 'Não'}</p>
                    <p class="col-span-2"><span class="text-orange-300">Valor:</span> R$ ${session.price.toFixed(2)}</p>
                </div>
            `;

            sessionContainer.appendChild(sessionCard);
        });
    } catch (error) {
        console.error('Erro ao carregar sessões:', error);
    }
};

sessionForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    try {
        const movieId = parseInt(document.getElementById('movieId').value);
        const movieResponse = await fetch(`/movie/${movieId}`);

        if (!movieResponse.ok) {
            throw new Error('Filme não encontrado');
        }

        const movieData = await movieResponse.json();
        const duration = movieData.movie.duration;
        const startTime = document.getElementById('startTime').value;

        const endTime = calculateEndTime(startTime, duration);

        const sessionData = {
            movie_id: movieId,
            room_number: parseInt(document.getElementById('roomNumber').value),
            start_time: startTime + ':00',
            end_time: endTime + ':00',
            price: parseFloat(document.getElementById('sessionValue').value),
            language: document.getElementById('language').value,
            subtitles: selectedRadio === 'yes'
        };

        console.log(sessionData)

        const response = await fetch('/session', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(sessionData)
        });

        if (response.ok) {
            await loadSessions();
            sessionForm.reset();
            selectedRadio = '';
        } else {
            const error = await response.json();
            alert(`Erro: ${error.detail}`);
        }
    } catch (error) {
        console.error('Erro:', error);
        alert(error.message);
    }
});

document.querySelector('#sessionList').addEventListener('click', async (e) => {
    if (e.target.classList.contains('edit-btn')) {
        const session = JSON.parse(e.target.dataset.session);
        const editModal = document.getElementById('edit-modal');

        document.getElementById('movieIdEdited').value = session.movie_id;
        document.getElementById('roomNumberEdited').value = session.room_number;
        document.getElementById('startTimeEdited').value = session.start_time;
        document.getElementById('sessionValueEdited').value = session.price;
        document.getElementById('languageEdited').value = session.language;
        document.getElementById('session_id_edited').value = session.id;

        document.querySelectorAll('input[name="subtitlesEdited"]').forEach(radio => {
            radio.checked = (session.subtitles && radio.value === 'yes') ||
                            (!session.subtitles && radio.value === 'no');
        });

        editModal.classList.remove('hidden');
    }
});

editSessionForm.addEventListener('submit', async (event) => {
    event.preventDefault();

        const movieId =  parseInt(document.getElementById('movieIdEdited').value);
        const movieResponse = await fetch(`/movie/${movieId}`);

        if (!movieResponse.ok) {
            throw new Error('Filme não encontrado');
        }

        const movieData = await movieResponse.json();
        const duration = movieData.movie.duration;
        const startTime = document.getElementById('startTimeEdited').value;

        const endTime = calculateEndTime(startTime, duration);

    const sessionData = {
        movie_id: parseInt(document.getElementById('movieIdEdited').value),
        room_number: parseInt(document.getElementById('roomNumberEdited').value),
        start_time: document.getElementById('startTimeEdited').value + ':00',
        end_time: endTime + ':00',
        price: parseFloat(document.getElementById('sessionValueEdited').value),
        language: document.getElementById('languageEdited').value,
        subtitles: selectedRadioEdited === 'yes'
    };

    const sessionId = document.getElementById('session_id_edited').value;

    try {
        const response = await fetch(`/session/${sessionId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(sessionData)
        });

        if (response.ok) {
            await loadSessions();
            document.getElementById('edit-modal').classList.add('hidden');
        } else {
            const error = await response.json();
            alert(`Erro: ${error.detail}`);
        }
    } catch (error) {
        console.error('Erro:', error);
    }
});

document.querySelector('#sessionList').addEventListener('click', async (e) => {
    if (e.target.classList.contains('delete-btn')) {
        const sessionId = e.target.dataset.id;
        const overlay = document.getElementById('dialog-overlay');
        overlay.classList.remove('hidden');

        document.getElementById('dialog-confirm').onclick = async () => {
            try {
                const response = await fetch(`/session/${sessionId}`, { method: 'DELETE' });
                if (response.ok) await loadSessions();
                overlay.classList.add('hidden');
            } catch (error) {
                console.error('Erro ao excluir sessão:', error);
            }
        };

        document.getElementById('dialog-cancel').onclick = () => {
            overlay.classList.add('hidden');
        };
    }
});

document.querySelector('#edit-modal').addEventListener('click', (e) => {
    if (e.target.closest('#edit-modal') && !e.target.closest('form')) {
        document.getElementById('edit-modal').classList.add('hidden');
    }
});

document.addEventListener('DOMContentLoaded', loadSessions);