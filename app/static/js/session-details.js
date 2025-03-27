const headerMovieTitle = document.querySelector("#headerMovieTitle");
const headerMovieSynopsis = document.querySelector("#headerMovieSynopsis");
const headerMovieImage = document.querySelector("#headerMovieImage");
const headerMovieDuration = document.querySelector("#headerMovieDuration");
const movieDuration = document.querySelector("#movieDuration");
const headerSessionDate = document.querySelector("#headerSessionDate");
const sessionHeader = document.querySelector("#sessionHeader");
const sessionSection = document.querySelector("#sessionSection");

const movieGenre = document.getElementById('movieGenre');
const movieRating = document.getElementById('movieRating');
const movieDirector = document.getElementById('movieDirector');
const sessionDateElement = document.getElementById('sessionDate');
const sessionTimeElement = document.getElementById('sessionTime');
const sessionRoomElement = document.getElementById('sessionRoom');
const sessionLanguageElement = document.getElementById('sessionLanguage');
const sessionSubtitlesElement = document.getElementById('sessionSubtitles');
const sessionPriceElement = document.getElementById('sessionPrice');
const movieRelease = document.getElementById('movieRelease');

const loadSessions = async () => {
    try {
        const pathSegments = window.location.pathname.split('/');
        const sessionId = pathSegments[pathSegments.length - 1];

        const sessionResponse = await fetch(`/session/${sessionId}`);
        const sessionData = await sessionResponse.json();
        const session = sessionData.session;

        const movieResponse = await fetch(`/movie/${session.movie_id}`);
        const movieData = await movieResponse.json();
        const movie = movieData.movie;

        headerMovieTitle.innerHTML = movie.title;
        headerMovieSynopsis.innerHTML = movie.synopsis;
        headerMovieImage.src = `/movie/${movie.id}/image/poster`;
        sessionHeader.classList.add(`bg-[url('/movie/${movie.id}/image/backdrop')]`);

        movieGenre.textContent = movie.genre;
        movieRating.textContent = `${movie.age_rating}+`;
        movieDirector.textContent = movie.director;

        const sessionDate = new Date(session.start_time);
        const options = {
            day: 'numeric',
            month: 'long',
            year: 'numeric',
            timeZone: 'America/Sao_Paulo'
        };

        const hours = Math.floor(movie.duration / 60);
        const minutes = movie.duration % 60;
        headerMovieDuration.textContent = `${hours}h ${minutes.toString().padStart(2, '0')}min`;
        movieDuration.textContent = `${hours}h ${minutes.toString().padStart(2, '0')}min`;
        headerSessionDate.textContent = sessionDate.toLocaleDateString('pt-BR', options);

        const startTime = new Date(session.start_time);
        const endTime = new Date(session.end_time);
        const releaseDate = new Date(movie.release_date);

        sessionDateElement.textContent = startTime.toLocaleDateString('pt-BR', {
            day: '2-digit',
            month: 'long',
            year: 'numeric'
        });

        sessionTimeElement.textContent = `${startTime.toLocaleTimeString('pt-BR', {
            hour: '2-digit',
            minute: '2-digit'
        })} - ${endTime.toLocaleTimeString('pt-BR', {
            hour: '2-digit',
            minute: '2-digit'
        })}`;

        sessionRoomElement.textContent = session.room_number;
        sessionLanguageElement.textContent = session.language;
        sessionSubtitlesElement.textContent = session.subtitles ? 'Português' : 'Não';
        sessionPriceElement.textContent = `R$ ${session.price.toFixed(2)}`;
        movieRelease.textContent = releaseDate.toLocaleDateString('pt-BR', options);

        const oldReserveButtonContainer = document.getElementById('reserveButtonContainer');
        if (oldReserveButtonContainer) {
            oldReserveButtonContainer.remove();
        }

        const reserveButtonContainer = document.createElement('div');
        reserveButtonContainer.id = 'reserveButtonContainer';
        reserveButtonContainer.className = 'flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-stone-800';
        reserveButtonContainer.innerHTML = `
            <button class="reserve-btn bg-orange-400 hover:bg-orange-500 text-stone-900 font-semibold py-3 px-8 rounded-lg transition-all duration-300 hover:scale-[1.02]"
                data-session="${JSON.stringify(session).replace(/"/g, '&quot;')}">
                Reservar Ingresso
            </button>
        `;

        sessionSection.appendChild(reserveButtonContainer);

        document.querySelector('#sessionSection').addEventListener('click', async (e) => {
            const accessToken = localStorage.getItem('access_token');
            if (!accessToken) {
                alert('Por favor, faça login para reservar ingressos');
                window.location.href = '/login-customer';
                return;
            }

            if (e.target.classList.contains('reserve-btn')) {
                const session = JSON.parse(e.target.dataset.session);
                console.log(session);
                const overlay = document.getElementById('dialog-overlay');

                try {
                    const response = await fetch(`/seat/room-number/${session.room_number}`);
                    const data = await response.json();
                    const availableSeats = data.seats.filter(seat => seat.is_available);

                    if (availableSeats.length === 0) {
                        alert('Não há assentos disponíveis nesta sessão!');
                        return;
                    }

                    const randomSeat = availableSeats[Math.floor(Math.random() * availableSeats.length)];

                    overlay.classList.remove('hidden');
                    document.getElementById('dialog-message').innerHTML = `
                        <div class="text-center space-y-4">
                            <h3 class="text-orange-400 font-bold text-lg">Confirmação de Reserva</h3>
                            <div class="text-red-100 space-y-2">
                                <p>Assento: <span class="font-bold">${randomSeat.seat_number}</span></p>
                                <p>Valor Total: <span class="text-green-400 font-bold">R$ ${session.price.toFixed(2)}</span></p>
                            </div>
                            <p class="text-sm text-stone-400">Deseja confirmar a reserva?</p>
                        </div>
                    `;
                    document.getElementById('dialog-confirm').onclick = async () => {
                        try {
                            const ticketResponse = await fetch('/ticket', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({
                                    session_id: parseInt(session.id),
                                    customer_id: localStorage.getItem('id'),
                                    seat_number: randomSeat.seat_number,
                                    price: parseFloat(session.price),
                                    status: "Confirmado"
                                })
                            });
                            if (!ticketResponse.ok) {
                                const error = await ticketResponse.json();
                                throw new Error(error.detail);
                            }
                            const seatResponse = await fetch(`/seat/${randomSeat.seat_number}`, {
                                method: 'PATCH',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({is_available: false})
                            });

                            if (!seatResponse.ok) {
                                const error = await seatResponse.json();
                                throw new Error(error.detail);
                            }
                            await loadSessions();
                        } catch (error) {
                            console.error('Erro:', error);
                            alert(`Erro: ${error.message}`);
                        } finally {
                            overlay.classList.add('hidden');
                        }
                    };
                    document.getElementById('dialog-cancel').onclick = () => {
                        overlay.classList.add('hidden');
                    };
                } catch (error) {
                    console.error('Erro:', error);
                    alert('Erro ao processar reserva');
                }
            }
        });
    } catch (error) {
        console.error('Erro ao carregar sessões:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadSessions);
