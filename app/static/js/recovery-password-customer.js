document.getElementById('reset-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {
        email: formData.get('email'),
        new_password: formData.get('password'),
    };

    try {
        const response = await fetch('/customer/reset-password', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const responseData = await response.json();
        console.log(responseData);

        if (response.ok) {
            alert('Senha redefinida com sucesso!');
            window.location.href = '/login-customer';

        } else {
            if (response.status === 401) {
                alert('Usuário não encontrado!');
            } else {
                alert(`Erro: ${responseData.detail || 'Erro desconhecido'}`);
            }
        }
    } catch (e) {
        console.error('Erro na requisição:', e);
        alert('Erro de conexão com o servidor');
    }
});