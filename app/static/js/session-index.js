const headerMovieTitle = document.querySelector("#headerMovieTitle");
const headerMovieSynopsis = document.querySelector("#headerMovieSynopsis");
const headerMovieImage = document.querySelector("#headerMovieImage");
const headerMovieDuration = document.querySelector("#headerMovieDuration");
const headerSessionDate = document.querySelector("#headerSessionDate");
const sessionHeader = document.querySelector("#sessionHeader");
const seeAllSessionsBtn = document.querySelector("#seeAllSessionsBtn");

seeAllSessionsBtn.addEventListener("click", async () => {
    window.location.href = "/session-customer";
})

const loadSessions = async () => {
    try {
        const response = await fetch('/session/all');
        const data = await response.json();
        const sessions = data.sessions;
        const sessionContainer = document.querySelector('#sessionList');
        sessionContainer.innerHTML = '';

        const firstSession = sessions[0];
        console.log(firstSession);

        const movieResponse = await fetch(`/movie/${firstSession.movie_id}`);
        const movieData = await movieResponse.json();
        const movie = movieData.movie;

        headerMovieTitle.innerHTML = movie.title;
        headerMovieSynopsis.innerHTML = movie.synopsis;
        headerMovieImage.src = `/movie/${movie.id}/image/poster`
        sessionHeader.classList.add(`bg-[url('/movie/${movie.id}/image/backdrop')]`);

        const sessionDate = new Date(firstSession.start_time);
        const options = {
            day: 'numeric',
            month: 'long',
            year: 'numeric',
            timeZone: 'America/Sao_Paulo'
        };
        headerSessionDate.textContent = sessionDate.toLocaleDateString('pt-BR', options);

        const hours = Math.floor(movie.duration / 60);
        const minutes = movie.duration % 60;
        headerMovieDuration.textContent = `${hours}h ${minutes.toString().padStart(2, '0')}min`;

        for (const session of sessions.slice(1, 4)) {
            const movieResponse = await fetch(`/movie/${session.movie_id}`);
            const movieData = await movieResponse.json();
            const movie = movieData.movie;

            const sessionCard = document.createElement('div');
            sessionCard.className = 'bg-stone-900 flex max-w-100 rounded-xl p-6 shadow-xl transition duration-300 mb-6';

            sessionCard.innerHTML = `
                <div class="flex flex-col items-center gap-6 group">
                    <div class="relative w-50 overflow-hidden rounded-xl border-2 border-stone-700">
                        <img src="/movie/${movie.id}/image/poster" 
                             alt="${movie.title}" 
                             class="w-full h-64 object-cover object-center transform group-hover:scale-105 transition duration-300">
                        <div class="absolute bottom-2 left-1/2 -translate-x-1/2">
                            <span class="bg-stone-900/80 px-3 py-1 rounded-full text-sm text-red-100 border border-stone-700">
                                ${movie.age_rating}+
                            </span>
                        </div>
                    </div>
            
                    <div class="flex-1 space-y-3">
                        <div class="flex flex-col flex-row items-center justify-between gap-3">
                            <h3 class="text-orange-400 text-2xl font-bold tracking-tight">${movie.title}</h3>
                            <span class="bg-stone-800 px-4 py-1.5 rounded-full text-sm text-red-100 border border-stone-700">
                                ${new Date(session.start_time).toLocaleDateString('pt-BR', {
                weekday: 'short',
                day: '2-digit',
                month: 'short'
            })}
                            </span>
                        </div>
            
                        <div class="grid grid-cols-1 grid-cols-2 gap-x-6 gap-y-4 text-red-100">
                            <div class="space-y-3">
                                <div class="flex items-center gap-2">
                                    <svg class="w-5 h-5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
                                    </svg>
                                    <span>Sala ${session.room_number}</span>
                                </div>
                                
                                <div class="flex items-center gap-2">
                                    <svg class="w-5 h-5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                    </svg>
                                    <span>${new Date(session.start_time).toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit'
            })} - ${new Date(session.end_time).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})}</span>
                                </div>
                            </div>
            
                            <div class="space-y-3">
                                <div class="flex items-center gap-2">
                                    <svg class="w-5 h-5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/>
                                    </svg>
                                    <span>${session.language} ${session.subtitles ? '+ Legendas' : ''}</span>
                                </div>
                                
                                <div class="flex items-center gap-2">
                                    <svg class="w-5 h-5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                                    </svg>
                                    <span>${movie.genre} • ${movie.duration} min</span>
                                </div>
                            </div>
                        </div>
            
                        <div class="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-stone-800">
                            <div class="flex items-center">
                                <span class="text-xl font-bold text-orange-400">R$ ${session.price.toFixed(2)}</span>
                            </div>
                            <button class="reserve-btn bg-orange-400 hover:bg-orange-500 text-stone-900 font-semibold py-3 px-8 rounded-lg transition-all duration-300 hover:scale-[1.02]"
                            data-session="${JSON.stringify(session).replace(/"/g, '&quot;')}"
                            >
                                Reservar Ingresso
                            </button>
                            <a href="/session-details/${session.id}"
                             class="details-btn border-2 border-orange-400 hover:border-orange-500 text-orange-400 hover:text-orange-500 font-semibold py-3 px-6 rounded-lg transition-all duration-300 hover:scale-[1.02] text-center text-sm text-base">
                                Ver Detalhes
                            </a>
                        </div>
                    </div>
                </div>
            `;
            sessionContainer.appendChild(sessionCard);
        }

        document.querySelector("#buyFirstSessionTicket").addEventListener("click", async () => {
            const accessToken = localStorage.getItem('access_token');
            if (!accessToken) {
                alert('Por favor, faça login para reservar ingressos');
                window.location.href = '/login-customer';
                return;
            }

            const sessionResponse = await fetch('/session/1');
            const sessionData = await sessionResponse.json();
            const session = sessionData.session;

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
            } catch (e) {
                console.error('Erro:', error);
                alert('Erro ao processar reserva');
            }
        });


        document.querySelectorAll('.reserve-btn').forEach(button => {
            button.addEventListener('click', async (e) => {
                const accessToken = localStorage.getItem('access_token');
                if (!accessToken) {
                    alert('Por favor, faça login para reservar ingressos');
                    window.location.href = '/login-customer';
                    return;
                }

                const session = JSON.parse(e.target.dataset.session);
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
            });
        });
    } catch (error) {
        console.error('Erro ao carregar sessões:', error);
    }
}


document.addEventListener('DOMContentLoaded', loadSessions);