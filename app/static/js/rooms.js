const roomForm = document.querySelector('#roomForm');
const editRoomForm = document.querySelector('#editRoomForm');


roomForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const roomData = {
        number: document.getElementById('roomNumber').value,
        capacity: document.getElementById('capacity').value,
    };

    try {
        const response = await fetch('/room', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(roomData)
        });

        const result = await response.json();

        if (response.ok) {
            await loadRooms()
            roomForm.reset();
        } else {
            alert(`Erro: ${result.detail}`);
        }
    } catch (error) {
        console.error('Erro:', error);
    }
});

const loadRooms = async () => {
    try {
        const response = await fetch('/room');
        const data = await response.json();
        const rooms = data.rooms;

        console.log(rooms);

        const roomContainer = document.querySelector('.room-container');
        roomContainer.innerHTML = '';

        rooms.forEach(room => {
            const roomCard = document.createElement('div');
            roomCard.classList.add('card');


            roomCard.innerHTML = `
                    <div class="card-header">
                        <h3>${room.number}</h3>
                    </div>
                    <div class="card-body">
                        <p><strong>ID:</strong> ${room.id}</p>
                        <p><strong>Número:</strong> ${room.capacity}</p>
                    </div>
                    <div id="rowConfig">
                        <img class="delete-btn" src="../static/icons/ic-trash.png" alt="" data-id="${room.id}""/>
                        <img class="edit-btn" src="../static/icons/ic-edit.png" alt="" data-room="${JSON.stringify(room).replace(/"/g, '&quot;')}"/>
                    </div>
            `;

            roomContainer.appendChild(roomCard);
        });
    } catch (error) {
        console.error('Erro ao carregar salas:', error);
    }
}

document.querySelector('.room-container').addEventListener('click', async (e) => {
    if (e.target && e.target.classList.contains('delete-btn')) {
        const roomId = e.target.dataset.id;

        const overlay = document.getElementById('dialog-overlay');

        overlay.classList.remove('hidden');


        document.getElementById('dialog-confirm').onclick = async () => {
            try {
                const response = await fetch(`/room?id=${roomId}`, {method: 'DELETE'});

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

document.querySelector('.room-container').addEventListener('click', async (e) => {
    if (e.target && e.target.classList.contains('edit-btn')) {
        const roomData = JSON.parse(e.target.dataset.room);

        document.getElementById('number_edited').value = roomData.number;
        document.getElementById('capacity_edited').value = roomData.capacity;

        document.getElementById('room_id_edited').value = roomData.id;

        document.getElementById('edit-modal').classList.remove('hidden');
    }
});

editRoomForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const roomId = document.getElementById('room_id_edited').value;

    const roomData = {
        number: document.getElementById('number_edited').value ,
        capacity: document.getElementById('capacity_edited').value,

    };

    try {
        const response = await fetch(`/room?id=${roomId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(roomData)
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