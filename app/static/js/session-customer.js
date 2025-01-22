const sessionContainer = document.querySelector('.session-container');


const loadSessions = async () => {
    try {
        const response = await fetch('/session');
        const data = await response.json();
        const sessions = data.sessions;
        sessionContainer.innerHTML = '';

        sessions.forEach(session => {
            const sessionCard = document.createElement('div');
            sessionCard.classList.add('card');

            sessionCard.innerHTML = `
                    <div class="card-header">
                        <h3 class="session-id" data-sid="${session.id}">${session.id}</h3>
                    </div>
                    <div class="card-body">
                        <p><strong>ID do filme:</strong> ${session.movie_id}</p>
                        <p><strong>Número da sala:</strong> ${session.room_number}</p>
                        <p><strong>Inicio:</strong> ${session.start_time}</p>
                        <p><strong>Fim:</strong> ${session.end_time}</p>
                        <p class="session-price" data-price="${session.price}"><strong >Valor da sessão (R$):</strong> ${session.price}</p>
                        <p><strong>Idioma do filme:</strong> ${session.language}</p>
                        <p><strong>Com legendas:</strong> ${session.subtitles ? 'Sim' : 'Não'}</p>
                    </div>
            `;

            sessionContainer.appendChild(sessionCard);
        });
        document.querySelectorAll('.card').forEach((element) => {
            element.addEventListener('click', async (e) => {
                const clickedElement = e.currentTarget;
                console.log(clickedElement);
                const sessionId = clickedElement.querySelector('.session-id').dataset.sid
                const sessionPrice = clickedElement.querySelector('.session-price').dataset.price
                await makeReservation(sessionId, sessionPrice, "Confirmado");
            });
        });

    } catch (error) {
        console.error('Error to  load sessions', error);
    }
}

const makeReservation = async (sessionId, price, status) => {
    document.querySelector('.session-container').addEventListener('click', async (e) => {
        if (e.target) {
            document.getElementById('dialog-confirm').onclick = async () => {
                const customerId = sessionStorage.getItem('userId');

                const ticketData = {
                    session_id: parseInt(sessionId),
                    customer_id: customerId,
                    seat_number: parseInt(randomSeatNumber(1, 200)),
                    price: parseFloat(price),
                    status: status
                };

                try {
                    const response = await fetch('/ticket', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(ticketData)
                    });

                    const result = await response.json();

                    if (response.ok) {
                        await loadSessions()
                        alert('The Registration was successfully sent.')
                    } else {
                        alert(`Error: ${result.detail}`);
                    }
                } catch (error) {
                    console.error('Error:', error);
                } finally {
                    overlay.classList.add('hidden');
                }
            };

            const overlay = document.getElementById('dialog-overlay');
            overlay.classList.remove('hidden');
            document.getElementById('dialog-cancel').onclick = () => {
                overlay.classList.add('hidden');
            };
        }
    });
}

const randomSeatNumber = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

document.addEventListener('DOMContentLoaded', loadSessions);