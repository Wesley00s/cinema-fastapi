document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        first_name: document.getElementById('first_name').value,
        last_name: document.getElementById('last_name').value,
        age: document.getElementById('age').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        address: document.getElementById('address').value,
        city: document.getElementById('city').value,
        state: document.getElementById('state').value,
        zip_code: document.getElementById('zip_code').value,
        country: document.getElementById('country').value
    };

    try {
        const response = await fetch('/customer', {
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
                const imageUpload = new Promise(async (resolve, reject) => {
                    const reader = new FileReader();
                    reader.onload = async function(e) {
                        try {
                            const imageResponse = await fetch('/customer/image', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    customer_id: result.customer.id,
                                    image_data: e.target.result
                                })
                            });

                            if (!imageResponse.ok) {
                                const error = await imageResponse.json();
                                reject("Erro na imagem: " + error.detail);
                            }
                            resolve();
                        } catch (error) {
                            reject(error);
                        }
                    };
                    reader.onerror = () => reject("Erro ao ler arquivo");
                    reader.readAsDataURL(fileInput.files[0]);
                });

                await imageUpload;
            }

            localStorage.setItem('access_token', result.access_token);
            localStorage.setItem('email', result.customer.email);
            window.location.href = '/';
        } else {
            const error = await response.json();
            alert('Erro no cadastro: ' + error.detail);
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Falha na conexão com o servidor');
    }
});

document.getElementById('photo').addEventListener('change', function () {
    const preview = document.getElementById('preview-image');
    const file = this.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
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
