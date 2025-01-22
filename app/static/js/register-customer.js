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
            const userResponse = await fetch(`/customer/email?email=${data.email}`);
            const userData = await userResponse.json();
            sessionStorage.setItem('userId', userData.customer.id);

            window.location.href = '/home-customer';
        } else {
            const error = await response.json();
            console.log('Error: ' + error.detail);
            alert('An error occurred while creating customer account.');
        }
    } catch (e) {
        console.log('Occurred an unexpected error: ' + e.message);
    }
});

