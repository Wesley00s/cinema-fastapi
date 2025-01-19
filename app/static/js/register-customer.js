document.getElementById('register-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/customer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            window.location.href = '/home';
        } else {
            const error = await response.json();
            console.log('Erro: ' + error.detail);
        }
    } catch (e) {
        console.log('Ocorreu um erro inesperado: ' + e.message);
    }
});

