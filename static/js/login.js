/**
 * Este archivo JavaScript contiene la lógica para manejar el formulario de inicio de sesión de usuarios.
 * Realiza el envío del formulario mediante AJAX y gestiona la respuesta del servidor.
 */

/**
 * Agrega un listener al formulario de inicio de sesión para interceptar el evento 'submit'.
 * Esto permite manejar el envío del formulario mediante AJAX y evitar el comportamiento
 * de envío por defecto del navegador.
 */
document.getElementById('loginForm').addEventListener('submit', function(event) {
    /**
     * Previene el comportamiento de envío por defecto del formulario.
     */
    event.preventDefault();

    /**
     * Obtiene el valor del campo de correo electrónico (nombre de usuario).
     */
    const username = document.getElementById('username').value;
    /**
     * Obtiene el valor del campo de contraseña.
     */
    const password = document.getElementById('password').value;

    /**
     * Realiza una petición AJAX al servidor para procesar el inicio de sesión.
     * 
     * La petición se envía a la URL obtenida dinámicamente mediante Django,
     * utilizando el método POST. Se incluyen las cabeceras necesarias para
     * el tipo de contenido JSON y el token CSRF.
     */
    fetch(document.getElementById('loginForm').action, { //Se obtiene la action del form
        method: 'POST',
        headers: {
            /**
             * Especifica que el tipo de contenido es JSON.
             * Esto es necesario para que el servidor Django pueda procesar los datos correctamente.
             */
            'Content-Type': 'application/json',
            /**
             * Incluye el token CSRF (Cross-Site Request Forgery) para proteger contra ataques CSRF.
             * Se accede a el mediante el `{{ csrf_token }}` que es una etiqueta de django.
             */
            'X-CSRFToken': document.querySelector('input[name=csrfmiddlewaretoken]').value
        },
        /**
         * Envía los datos del formulario en el cuerpo de la solicitud.
         * Los datos se convierten a formato JSON.
         */
        body: JSON.stringify({ username: username, password: password })
    })
    /**
     * Procesa la respuesta del servidor.
     * Primero, convierte la respuesta a formato JSON.
     */
    .then(response => response.json())
    /**
     * Luego, maneja los datos recibidos.
     *
     * @param {object} data - Datos recibidos del servidor en formato JSON.
     *                        Puede contener 'message' o 'error'.
     */
    .then(data => {
        /**
         * Obtiene el elemento HTML donde se mostrarán los mensajes de error.
         */
        const mensajeDiv = document.getElementById('mensaje');
        /**
         * Obtiene el elemento HTML donde se mostrarán los mensajes de éxito.
         */
        const successDiv = document.getElementById('success');
        /**
         * Verifica si el mensaje recibido indica un inicio de sesión exitoso.
         */
        if (data.message == 'Login exitoso') {
            /**
             * Muestra el mensaje de éxito en el elemento correspondiente.
             */
            successDiv.textContent = data.message;
            /**
             * Establece la clase CSS para el mensaje de éxito.
             */
            successDiv.className = 'mt-3 text-center text-success';
            /**
             * Redirige al usuario a la página de administración de usuarios.
             */
            window.location.href = "/usuarios/admin_usuarios/";
        } else if (data.error) {
            /**
             * Muestra el mensaje de error en el elemento correspondiente.
             */
            mensajeDiv.textContent = data.error;
            /**
             * Establece la clase CSS para el mensaje de error.
             */
            mensajeDiv.className = 'mt-3 text-center text-danger';
        }
    })
    /**
     * Captura y maneja errores en la petición AJAX.
     */
    .catch(error => {
        console.error('Error:', error);
        /**
         * Obtiene el elemento HTML donde se mostrarán los mensajes de error.
         */
        const mensajeDiv = document.getElementById('mensaje');
        /**
         * Muestra un mensaje de error genérico al usuario.
         */
        mensajeDiv.textContent = 'Ocurrió un error inesperado.';
        /**
         * Establece la clase CSS para el mensaje de error.
         */
        mensajeDiv.className = 'mt-3 text-center text-danger';
    });
});
/**
 * Obtiene el elemento HTML donde se mostrarán los mensajes de error.
 */
const mensajeDiv = document.getElementById('mensaje');
/**
 * Obtiene el campo de nombre de usuario.
 */
const usernameInput = document.getElementById('username');
/**
 * Obtiene el campo de contraseña.
 */
const passwordInput = document.getElementById('password');

/**
 * Agrega un listener al campo de nombre de usuario para borrar el mensaje de error cuando se ingrese texto.
 */
usernameInput.addEventListener('input', function() {
    mensajeDiv.textContent = '';
});

/**
 * Agrega un listener al campo de contraseña para borrar el mensaje de error cuando se ingrese texto.
 */
passwordInput.addEventListener('input', function() {
    mensajeDiv.textContent = '';
});