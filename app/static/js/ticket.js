const ticketList = document.querySelector('#ticketList');


const loadTickets = async () => {
    try {
        const response = await fetch('/ticket/all');
        const data = await response.json();
        const tickets = data.tickets;
        ticketList.innerHTML = '';

        const total = tickets.reduce((acc, ticket) => acc + ticket.price, 0);
        document.getElementById('totalSales').textContent =
            `R$ ${total.toFixed(2).replace('.', ',')}`;

        tickets.forEach(ticket => {
            const ticketCard = document.createElement('div');
            ticketCard.className = `bg-stone-800 border-2 border-stone-700 rounded-xl max-w-80 p-4 shadow-lg
                hover:border-orange-400 hover:shadow-orange-400/20 hover:transform hover:scale-[1.02]
                transition-all duration-300 cursor-pointer`;

            ticketCard.innerHTML = `
                <div class="flex justify-between items-start mb-3 pb-3 border-b border-stone-600">
                    <div class="flex items-center gap-2">
                        <svg class="w-6 h-6 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"/>
                        </svg>
                        <h3 class="text-orange-400 font-bold text-lg">#${ticket.id}</h3>
                    </div>
                    <span class="px-2 py-1 text-sm rounded-full 
                        ${ticket.status === 'Confirmado' ?
                'bg-green-800/30 text-green-400 border border-green-600/50' :
                'bg-red-800/30 text-red-400 border border-red-600/50'}">
                        ${ticket.status}
                    </span>
                </div>
                
                <div class="grid grid-cols-2 gap-3 text-red-100">
                    <div class="flex items-center gap-2">
                        <svg class="w-5 h-5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                        </svg>
                        <span>Assento ${ticket.seat_number}</span>
                    </div>
                    
                    <div class="flex items-center gap-2">
                        <svg class="w-5 h-5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"/>
                        </svg>
                        <span>Sessão ${ticket.session_id}</span>
                    </div>
                    
                    <div class="flex items-center gap-2">
                        <svg class="w-5 h-5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                        </svg>
                        <span>Cliente #${ticket.customer_id}</span>
                    </div>
                    
                    <div class="flex items-center gap-2">
                        <svg class="w-5 h-5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                        <span>R$ ${ticket.price.toFixed(2)}</span>
                    </div>
                </div>
                
                <div class="mt-3 pt-3 border-t border-stone-600 text-sm text-stone-400">
                    <span class="flex items-center gap-1">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                        ${new Date(ticket.create_at).toLocaleString()}
                    </span>
                </div>
            `;

            ticketList.appendChild(ticketCard);
        });

    } catch (error) {
        console.error('Erro ao carregar bilhetes:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadTickets)