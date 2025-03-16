document.querySelector('.logout-btn').addEventListener('click', () => {
    localStorage.clear();
});

async function loadProfileData() {
    const email = localStorage.getItem('email');
    try {
        const response = await fetch(`/customer/email/${email}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });

        if (!response.ok) {
            if (response.status === 401) {
                localStorage.removeItem('access_token');
                window.location.href = '/login-customer';
                return;
            }
            throw new Error(`Erro HTTP: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);

        if (data.status === 'success') {
            const customer = data.customer;

            document.getElementById('user-name').textContent = `${customer.first_name} ${customer.last_name}`;
            document.getElementById('user-email').textContent = customer.email;
            document.getElementById('user-age').textContent = customer.age;
            document.getElementById('user-address').textContent = customer.address;
            document.getElementById('user-city').textContent = customer.city;
            document.getElementById('user-state').textContent = customer.state;
            document.getElementById('user-zip').textContent = customer.zip_code;
            document.getElementById('user-country').textContent = customer.country;

            const profilePhoto = document.getElementById('profile-photo');

            try {
                const imageResponse = await fetch(`/customer/${customer.id}/image`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    }
                });

                if (imageResponse.ok) {
                    const imageBlob = await imageResponse.blob();
                    const imageUrl = URL.createObjectURL(imageBlob);
                    profilePhoto.src = imageUrl;
                } else {
                    console.error('Erro ao carregar a imagem');
                    profilePhoto.src = '/static/icons/avatar.png';
                }
            } catch (imgError) {
                console.error('Erro ao buscar imagem:', imgError);
                profilePhoto.src = '/static/icons/avatar.png';
            }

            profilePhoto.onerror = function () {
                this.src = '/static/icons/avatar.png';
            };
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Falha ao carregar dados do perfil: ' + error.message);
    }
}

document.addEventListener('DOMContentLoaded', loadProfileData);
