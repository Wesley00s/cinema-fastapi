document.getElementById('register-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/admin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            window.location.href = '/home-admin';
        } else {
            const error = await response.json();
            console.log('Erro: ' + error.detail);
            alert('An error occurred while creating admin account.');
        }
    } catch (e) {
        console.log('Occurred an unexpected error: ' + e.message);
    }
});

