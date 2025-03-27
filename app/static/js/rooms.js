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
            await loadRooms();
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
        const response = await fetch('/room/all');
        const data = await response.json();
        const rooms = data.rooms;

        const roomContainer = document.querySelector('#roomList');
        roomContainer.innerHTML = '';

        rooms.forEach(room => {
            const roomCard = document.createElement('div');
            roomCard.className = 'bg-stone-900/90 border-2 border-stone-800 rounded-lg p-4';

            roomCard.innerHTML = `
                <div class="flex justify-between items-center mb-2">
                    <h3 class="text-orange-300 text-xl font-bold">Sala ${room.number}</h3>
                    <div class="flex gap-2">
                        <button class="delete-btn text-red-100 hover:text-orange-400 cursor-pointer hover:scale-150 transition duration-300"
                            data-id="${room.id}">🗑️</button>
                        <button class="edit-btn text-red-100 hover:text-orange-400 cursor-pointer hover:scale-150 transition duration-300"
                            data-room='${JSON.stringify(room).replace(/"/g, '&quot;')}'>✏️</button>
                    </div>
                </div>
                <div class="text-red-100 space-y-1">
                    <p><span class="text-orange-300">Capacidade:</span> ${room.capacity} lugares</p>
                    <p><span class="text-orange-300">ID:</span> ${room.id}</p>
                </div>
            `;

            roomContainer.appendChild(roomCard);
        });
    } catch (error) {
        console.error('Erro ao carregar salas:', error);
    }
}

document.querySelector('#roomList').addEventListener('click', async (e) => {
    if (e.target.classList.contains('delete-btn')) {
        const roomId = e.target.dataset.id;
        const overlay = document.getElementById('dialog-overlay');
        const dialogMessage = document.querySelector('#dialog-message');

        overlay.classList.remove('hidden');
        dialogMessage.textContent = 'Você tem certeza que deseja excluir esta sala?';

        document.getElementById('dialog-confirm').onclick = async () => {
            try {
                const response = await fetch(`/room/${roomId}`, {method: 'DELETE'});
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

document.querySelector('#roomList').addEventListener('click', async (e) => {
    if (e.target.classList.contains('edit-btn')) {
        try {
            const roomData = JSON.parse(e.target.dataset.room.replace(/&quot;/g, '"'));

            document.getElementById('number_edited').value = roomData.number;
            document.getElementById('capacity_edited').value = roomData.capacity;
            document.getElementById('room_id_edited').value = roomData.id;

            document.getElementById('edit-modal').classList.remove('hidden');
        } catch (error) {
            console.error('Erro ao parsear dados da sala:', error);
            alert('Erro ao carregar dados para edição');
        }
    }
});

editRoomForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const roomId = document.getElementById('room_id_edited').value;
    const roomData = {
        number: document.getElementById('number_edited').value,
        capacity: document.getElementById('capacity_edited').value
    };

    try {
        const response = await fetch(`/room/${roomId}`, {
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