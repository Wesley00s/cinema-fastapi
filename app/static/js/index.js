const decodeJwtPayload = (token) => {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        return JSON.parse(atob(base64));
    } catch (error) {
        return null;
    }
};

const isAdmin = () => {
    try {
        const accessToken = localStorage.getItem('access_token');
        const payload = decodeJwtPayload(accessToken);
        return payload.is_admin === true;
    } catch (error) {
        return false;
    }

}

console.log(isAdmin());

if (!isAdmin()) {
    const adminRoutes = ['/profile-admin', '/rooms', '/movies', '/tickets', '/sessions'];

    if (adminRoutes.includes(window.location.pathname)) {
        window.location.href = '/';
    }
}

const isLoginPage = () => {
    const baseRoutes = ['/login-customer', '/login-admin', '/register-customer', '/register-admin'];
       const currentPath = window.location.pathname;

    if (currentPath.startsWith('/session-details/')) {
        return true;
    }

    let noLoginRoutes = [...baseRoutes];
    if (localStorage.getItem('access_token') === null) {
        noLoginRoutes.push("/")
        noLoginRoutes.push("/session-customer")
    } else {
        noLoginRoutes.push("/profile-admin");
        noLoginRoutes.push("/rooms");
        noLoginRoutes.push("/movies");
        noLoginRoutes.push("/tickets");
        noLoginRoutes.push("/sessions");

    }
    return noLoginRoutes.includes(window.location.pathname);
};

const checkAccessToken = async () => {
    if (isLoginPage()) return;

    const accessToken = localStorage.getItem('access_token');

    if (!accessToken) {
        redirectToLogin();
        return;
    }

    const payload = decodeJwtPayload(accessToken);

    if (!payload?.exp) {
        console.error('Token inválido');
        redirectToLogin();
        return;
    }

    const expirationTime = payload.exp * 1000;
    if (Date.now() >= expirationTime) {
        alert('Sessão expirada');
        redirectToLogin();
        return;
    }

    localStorage.setItem('email', payload.sub);
    localStorage.setItem('id', payload.id);
};

const redirectToLogin = () => {
    if (!isLoginPage()) {
        localStorage.removeItem('access_token');
        window.location.href = '/';
    }
};

const updateNavigation = () => {
    if (isLoginPage()) return;

    const accessToken = localStorage.getItem('access_token');

    const desktopSelectContainer = document.querySelector('.relative.group');
    if (desktopSelectContainer) {
        desktopSelectContainer.innerHTML = accessToken ? `
            <a href="/profile-customer" class="text-red-100 hover:text-white/70 hover:scale-105 transition duration-300">
                Ver Perfil
            </a>
        ` : `
            <select
                onchange="window.location.href = this.value"
                class="appearance-none bg-transparent text-red-100 pl-4 pr-8 py-2 rounded-lg hover:text-white/70 cursor-pointer focus:outline-none focus:ring-2 focus:ring-orange-400 border border-transparent hover:border-stone-700 transition-all"
            >
                <option value="" class="bg-stone-900">Login</option>
                <option value="/login-customer" class="bg-stone-900">Sou Cliente</option>
                <option value="/login-admin" class="bg-stone-900">Sou Admin</option>
            </select>
        `;
    }

    const mobileMenu = document.querySelector('.peer-checked\\:block div');
    if (mobileMenu) {
        mobileMenu.innerHTML = accessToken ? `
            <a href="/session-customer" class="text-red-100 hover:text-white/70 hover:scale-105 transition duration-300">
                Ver sessões
            </a>
                        <a href="/profile-customer" class="text-red-100 hover:text-white/70 hover:scale-105 transition duration-300">
                Ver Perfil
            </a>
        ` : `
            <select
                onchange="window.location.href = this.value"
                class="bg-stone-900 text-red-100 p-2 rounded-lg border border-stone-700 focus:outline-none focus:ring-2 focus:ring-orange-400 hover:border-stone-600 transition-colors"
            >
                <option value="">Login</option>
                <option value="/login-customer">Sou Cliente</option>
                <option value="/login-admin">Sou Admin</option>
            </select>
        `;
    }
};

document.addEventListener('DOMContentLoaded', async () => {
    await checkAccessToken();
    updateNavigation();
});