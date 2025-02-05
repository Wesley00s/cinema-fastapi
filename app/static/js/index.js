const decodeJwtPayload = (token) => {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        return JSON.parse(atob(base64));
    } catch (error) {
        return null;
    }
};

const checkAccessToken = async () => {
    const accessToken = localStorage.getItem('access_token');

    if (!accessToken) {
        redirectToLogin();
        localStorage.clear();
        return;
    }

    const payload = decodeJwtPayload(accessToken);

    if (!payload || !payload.exp) {
        console.error('Invalid token');
        localStorage.clear();
        redirectToLogin();
    }

    const expirationTime = payload.exp * 1000;
    if (Date.now() >= expirationTime) {
        alert('Session has expired');
        localStorage.clear();
        redirectToLogin();
    }

    localStorage.setItem('email', payload.sub);
    localStorage.setItem('id', payload.id);
};

const redirectToLogin = () => {
    localStorage.removeItem('access_token');
    window.location.href = '/';
};

document.addEventListener('DOMContentLoaded', checkAccessToken);
