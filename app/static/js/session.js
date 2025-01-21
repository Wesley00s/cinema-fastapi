const sessionForm = document.querySelector('#sessionForm');
const editRoomForm = document.querySelector('#editRoomForm');
const radios = document.getElementsByName('subtitles')
let selectedRadio = '';

radios.forEach(radio => {
    radio.addEventListener('change', (e) => {
        console.log(radio.value);
        selectedRadio = radio.value;
    })
})
const formatDate = (isoString) => {
    const date = new Date(isoString);
    return date.toISOString().replace('T', ' ').substring(0, 23);
}

sessionForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const sessionData = {
        movie_id: parseInt(document.getElementById('movieId').value),
        room_id: parseInt(document.getElementById('roomId').value),
        start_time: formatDate(document.getElementById('startTime').value),
        end_time: formatDate(document.getElementById('endTime').value),
        price: parseFloat(document.getElementById('sessionValue').value),
        language: document.getElementById('language').value,
        subtitles: selectedRadio === 'yes',
    };

    console.log(sessionData);

    try {
        const response = await fetch('/session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(sessionData)
        });

        const result = await response.json();

        if (response.ok) {
            await loadRooms()
            sessionForm.reset();
        } else {
            alert(`Erro: ${result.detail}`);
        }
    } catch (error) {
        console.error('Erro:', error);
    }
});

const loadRooms = async () => {
    try {
        const response = await fetch('/session');
        const data = await response.json();
        const sessions = data.sessions;

        console.log(sessions);

        const sessionContainer = document.querySelector('.session-container');
        sessionContainer.innerHTML = '';

        sessions.forEach(session => {
            const sessionCard = document.createElement('div');
            sessionCard.classList.add('card');

            sessionCard.innerHTML = `
                    <div class="card-header">
                        <h3>${session.number}</h3>
                    </div>
                    <div class="card-body">
                        <p><strong>ID:</strong> ${session.id}</p>
                        <p><strong>Número:</strong> ${session.capacity}</p>
                    </div>
                    <div id="rowConfig">
                        <img class="delete-btn" src="../static/icons/ic-trash.png" alt="" data-id="${session.id}""/>
                        <img class="edit-btn" src="../static/icons/ic-edit.png" alt="" data-session="${JSON.stringify(session).replace(/"/g, '&quot;')}"/>
                    </div>
            `;

            sessionContainer.appendChild(sessionCard);
        });
    } catch (error) {
        console.error('Erro ao carregar salas:', error);
    }
}

document.querySelector('.session-container').addEventListener('click', async (e) => {
    if (e.target && e.target.classList.contains('delete-btn')) {
        const sessionId = e.target.dataset.id;

        const overlay = document.getElementById('dialog-overlay');

        overlay.classList.remove('hidden');


        document.getElementById('dialog-confirm').onclick = async () => {
            try {
                const response = await fetch(`/session?id=${sessionId}`, {method: 'DELETE'});

                if (response.ok) {
                    await loadRooms();
                } else {
                    alert("Erro ao excluir a sala.");
                }
            } catch (error) {
                console.error('Erro ao excluir a sala:', error);
            } finally {
                overlay.classList.add('hidden');
            }
        };

        document.getElementById('dialog-cancel').onclick = () => {
            overlay.classList.add('hidden');
        };
    }
});

document.querySelector('.session-container').addEventListener('click', async (e) => {
    if (e.target && e.target.classList.contains('edit-btn')) {
        const sessionData = JSON.parse(e.target.dataset.session);

        document.getElementById('number_edited').value = sessionData.number;
        document.getElementById('capacity_edited').value = sessionData.capacity;

        document.getElementById('session_id_edited').value = sessionData.id;

        document.getElementById('edit-modal').classList.remove('hidden');
    }
});

editRoomForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const sessionId = document.getElementById('session_id_edited').value;

    const sessionData = {
        number: document.getElementById('number_edited').value,
        capacity: document.getElementById('capacity_edited').value,

    };

    try {
        const response = await fetch(`/session?id=${sessionId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(sessionData)
        });

        const result = await response.json();

        if (response.ok) {
            await loadRooms();
            editRoomForm.reset();
            document.getElementById('edit-modal').classList.add('hidden');
        } else {
            alert(`Erro: ${result.detail}`);
        }
    } catch (error) {
        console.error('Erro:', error);
    }
});

document.getElementById('close-modal').addEventListener('click', () => {
    document.getElementById('edit-modal').classList.add('hidden');
});


document.addEventListener('DOMContentLoaded', loadRooms);