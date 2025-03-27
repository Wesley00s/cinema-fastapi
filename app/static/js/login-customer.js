document.getElementById('login-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {
        email: formData.get('email'),
        password: formData.get('password')
    };
    localStorage.setItem('email', data.email);

    try {
        const response = await fetch('/customer/auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const responseData = await response.json();
        console.log(responseData);

        if (response.ok) {
            localStorage.setItem('access_token', responseData.access_token);
            window.location.href = '/';

        } else {
            if (response.status === 401) {
                alert('Credenciais inválidas');
            } else {
                alert(`Erro: ${responseData.detail || 'Erro desconhecido'}`);
            }
        }
    } catch (e) {
        console.error('Erro na requisição:', e);
        alert('Erro de conexão com o servidor');
    }
});