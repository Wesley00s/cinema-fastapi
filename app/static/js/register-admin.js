document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        first_name: document.getElementById('first_name').value,
        last_name: document.getElementById('last_name').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        address: document.getElementById('address').value,
        city: document.getElementById('city').value,
        state: document.getElementById('state').value,
        zip_code: document.getElementById('zip_code').value,
        country: document.getElementById('country').value
    };

    try {
        const response = await fetch('/admin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        if (response.ok) {
            const result = await response.json();

            const fileInput = document.getElementById('photo');
            if (fileInput.files[0]) {
                const reader = new FileReader();
                reader.onload = async function(e) {
                    const imageData = e.target.result;

                    const imagePayload = {
                        admin_id: result.admin.id,
                        image_data: imageData
                    };

                    const imageResponse = await fetch('/admin/image', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(imagePayload)
                    });

                    if (!imageResponse.ok) {
                        const errorImg = await imageResponse.json();
                        alert("Erro ao enviar imagem: " + errorImg.detail);
                    }
                };
                reader.readAsDataURL(fileInput.files[0]);
            }

            localStorage.setItem('access_token', result.access_token);
            localStorage.setItem('email', result.admin.email);
            window.location.href = '/home-admin';
        } else {
            const error = await response.json();
            alert('Erro no cadastro: ' + error.detail);
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Falha na conexão com o servidor');
    }
});

document.getElementById('photo').addEventListener('change', function() {
    const preview = document.getElementById('preview-image');
    const file = this.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
            document.getElementById('photo-preview').style.display = 'block';
        }
        reader.readAsDataURL(file);
    }
});

window.addEventListener('load', () => {
    const savedPhoto = localStorage.getItem('user_photo');
    if (savedPhoto) {
        const preview = document.getElementById('preview-image');
        preview.src = savedPhoto;
        preview.style.display = 'block';
        document.getElementById('photo-preview').style.display = 'block';
    }
});
