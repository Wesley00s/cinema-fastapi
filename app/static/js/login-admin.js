document.getElementById('login-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/admin/auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            await response.json();
            window.location.href = '/home-admin';
        } else {
            const error = await response.json();
            console.log('Erro: ' + error.detail);
            alert('Invalid login credentials or other error occurred.');
        }
    } catch (e) {
        console.log('Ocorreu um erro inesperado: ' + e.message);
    }
});
