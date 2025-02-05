document.querySelector('.logout-btn').addEventListener('click', () => {
    localStorage.clear();
});

async function loadProfileData() {
    const email = localStorage.getItem('email');
    try {
        const response = await fetch(`/admin/email?email=${email}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });

        if (!response.ok) {
            if (response.status === 401) {
                localStorage.removeItem('access_token');
                window.location.href = '/login-admin';
                return;
            }
            throw new Error(`Erro HTTP: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);

        if (data.status === 'success') {
            const admin = data.admin;

            document.getElementById('user-name').textContent = `${admin.first_name} ${admin.last_name}`;
            document.getElementById('user-email').textContent = admin.email;
            document.getElementById('user-address').textContent = admin.address;
            document.getElementById('user-city').textContent = admin.city;
            document.getElementById('user-state').textContent = admin.state;
            document.getElementById('user-zip').textContent = admin.zip_code;
            document.getElementById('user-country').textContent = admin.country;


            const imageResponse = await fetch(`/admin/${admin.id}/image`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            console.log(imageResponse);

            if (imageResponse.ok) {
                const imageBlob = await imageResponse.blob();
                const imageUrl = URL.createObjectURL(imageBlob);
                document.getElementById('profile-photo').src = imageUrl;
                console.log(imageUrl);
            } else {
                console.error('Erro ao carregar a imagem');
            }
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Falha ao carregar dados do perfil: ' + error.message);
    }
}

document.addEventListener('DOMContentLoaded', loadProfileData);
