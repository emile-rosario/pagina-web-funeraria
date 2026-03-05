/**
 * API Helper — Funeraria Rancier
 * Funciones centralizadas para comunicarse con el backend.
 */
const API_URL = "http://127.0.0.1:8000";


// ─────────────────────────────────────────────────────────────
// AUTENTICACIÓN
// ─────────────────────────────────────────────────────────────

/**
 * Iniciar sesión y guardar el token en localStorage.
 */
async function iniciarSesion(email, password) {
    try {
        const respuesta = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const resultado = await respuesta.json();

        if (respuesta.ok) {
            localStorage.setItem('token', resultado.access_token);
            localStorage.setItem('usuario', resultado.user_name);
            localStorage.setItem('usuario_rol', resultado.user_rol || 'cliente');

            alert(`¡Bienvenido de nuevo, ${resultado.user_name}!`);
            window.location.href = "dashboard.html";
        } else {
            alert("Error: " + (resultado.detail || "Credenciales incorrectas"));
        }
    } catch (error) {
        console.error("No hay conexión con el servidor:", error);
        alert("El servidor de la funeraria no responde. Asegúrate de que Uvicorn esté corriendo.");
    }
}

/**
 * Registrar un nuevo usuario.
 */
async function registrarUsuario(nombre, email, telefono, password) {
    try {
        const respuesta = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre, email, telefono, password })
        });

        const resultado = await respuesta.json();

        if (respuesta.ok) {
            alert(`¡Registro exitoso! Bienvenido, ${resultado.nombre}.`);
            window.location.href = "login.html";
        } else {
            alert("Error: " + (resultado.detail || "No se pudo registrar."));
        }
    } catch (error) {
        console.error("Error de conexión:", error);
        alert("El servidor no responde. Verifica que Uvicorn esté activo.");
    }
}


// ─────────────────────────────────────────────────────────────
// SESIÓN Y AUTORIZACIÓN
// ─────────────────────────────────────────────────────────────

/**
 * Obtener el token JWT guardado.
 */
function getToken() {
    return localStorage.getItem('token');
}

/**
 * Obtener los headers con el token de autorización.
 */
function getAuthHeaders() {
    const token = getToken();
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

/**
 * Verificar si el usuario está logueado.
 * Si no lo está, redirige al login.
 */
function requireAuth() {
    const token = getToken();
    if (!token) {
        alert("Debes iniciar sesión para acceder a esta página.");
        window.location.href = "login.html";
        return false;
    }
    return true;
}

/**
 * Verificar si el usuario es admin.
 */
function isAdmin() {
    return localStorage.getItem('usuario_rol') === 'admin';
}

/**
 * Obtener el nombre del usuario logueado.
 */
function getUsuarioNombre() {
    return localStorage.getItem('usuario') || 'Usuario';
}

/**
 * Cerrar sesión: limpia localStorage y redirige al login.
 */
function cerrarSesion() {
    localStorage.removeItem('token');
    localStorage.removeItem('usuario');
    localStorage.removeItem('usuario_rol');
    window.location.href = "login.html";
}


// ─────────────────────────────────────────────────────────────
// PETICIONES AL API
// ─────────────────────────────────────────────────────────────

/**
 * Obtener la lista de ataúdes desde el backend.
 */
async function obtenerAtaudes() {
    try {
        const respuesta = await fetch(`${API_URL}/ataudes`);
        if (respuesta.ok) {
            return await respuesta.json();
        }
        return [];
    } catch (error) {
        console.error("Error al obtener ataúdes:", error);
        return [];
    }
}

/**
 * Obtener la lista de planes funerarios desde el backend.
 */
async function obtenerPlanes() {
    try {
        const respuesta = await fetch(`${API_URL}/planes`);
        if (respuesta.ok) {
            return await respuesta.json();
        }
        return [];
    } catch (error) {
        console.error("Error al obtener planes:", error);
        return [];
    }
}

/**
 * Obtener el perfil del usuario autenticado.
 */
async function obtenerPerfil() {
    try {
        const respuesta = await fetch(`${API_URL}/me`, {
            headers: getAuthHeaders()
        });
        if (respuesta.ok) {
            return await respuesta.json();
        }
        return null;
    } catch (error) {
        console.error("Error al obtener perfil:", error);
        return null;
    }
}