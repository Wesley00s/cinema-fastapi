const ticketContainer = document.querySelector('.ticket-container');


const loadTickets = async () => {
    try {
        const response = await fetch('/ticket');
        const data = await response.json();
        const tickets = data.tickets;
        ticketContainer.innerHTML = '';

        tickets.forEach(ticket => {
            const ticketCard = document.createElement('div');
            ticketCard.classList.add('card');

            ticketCard.innerHTML = `
                    <div class="card-header">
                        <h3>${ticket.id}</h3>
                    </div>
                    <div class="card-body">
                        <p><strong>Numero do assento:</strong> ${ticket.seat_number}</p>
                        <p><strong>ID da sessão</strong> ${ticket.session_id}</p>
                        <p><strong>Cliente:</strong> ${ticket.customer_id}</p>
                        <p><strong>Preço:</strong> ${ticket.price}</p>
                        <p><strong>Status:</strong> ${ticket.status}</p>
                    </div>
            `;

            ticketContainer.appendChild(ticketCard);
        });

    } catch (error) {
        console.error('Error to  load tickets', error);
    }
}


document.addEventListener('DOMContentLoaded', loadTickets);