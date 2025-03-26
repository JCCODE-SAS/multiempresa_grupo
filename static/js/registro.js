/**
 * Este archivo JavaScript contiene la lógica para manejar el formulario de registro de usuarios.
 * Realiza la validación de datos y envía la solicitud al servidor.
 */

/**
 * Agrega un listener al formulario de registro para interceptar el evento 'submit'.
 * Esto permite manejar el envío del formulario mediante AJAX y evitar el comportamiento
 * de envío por defecto del navegador.
 */
document.getElementById('registroForm').addEventListener('submit', function(event) {
    /**
     * Previene el comportamiento de envío por defecto del formulario.
     */
    event.preventDefault();

    /**
     * Crea un objeto FormData a partir del formulario.
     * Esto facilita la recolección de todos los datos del formulario.
     */
    const formData = new FormData(this);
    /**
     * Crea un objeto URLSearchParams a partir del FormData.
     * Esto formatea los datos para ser enviados como una cadena de consulta (query string).
     */
    const data = new URLSearchParams(formData);

    /**
     * Realiza una petición AJAX al servidor para procesar el registro.
     * 
     * La petición se envía a la URL '/usuarios/registro/' mediante el método POST.
     * Se incluyen las cabeceras necesarias para el token CSRF y el tipo de contenido.
     */
    fetch('/usuarios/registro/', {
        method: 'POST',
        headers: {
            /**
             * Incluye el token CSRF (Cross-Site Request Forgery) para proteger contra ataques CSRF.
             * La función getCookie se utiliza para obtener el valor del token CSRF de las cookies.
             */
            'X-CSRFToken': getCookie('csrftoken'),
            /**
             * Especifica que el tipo de contenido es 'application/x-www-form-urlencoded'.
             * Esto es necesario para que el servidor Django pueda procesar los datos correctamente.
             */
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        /**
         * Envía los datos del formulario en el cuerpo de la solicitud.
         */
        body: data
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
     *                        Puede contener 'error' o 'message' en caso de exito.
     */
    .then(data => {
        /**
         * Obtiene el elemento HTML donde se mostrará la sugerencia de nombre de usuario.
         */
        const suggestionElement = document.getElementById('username-suggestion');
        /**
         * Limpia cualquier mensaje previo en el elemento de sugerencia.
         */
        suggestionElement.innerHTML = '';

        /**
         * Si el servidor devuelve un error.
         */
        if (data.error) {
            /**
             * Si el error específico es que el nombre de usuario ya está en uso y hay una sugerencia.
             */
            if (data.error === "El nombre de usuario ya está en uso" && data.sugerencia) {
                /**
                 * Muestra el mensaje de error y la sugerencia en el contenedor de sugerencias.
                 * Se crea un enlace para la sugerencia y se añade al contenedor.
                 */
                suggestionElement.innerHTML = `${data.error}. Sugerencia: <a href="#" id="username-suggestion-link">${data.sugerencia}</a>`;
                suggestionElement.style.display = 'block';

                /**
                 * Agrega un evento de clic al enlace de sugerencia.
                 */
                document.getElementById('username-suggestion-link').addEventListener('click', function(event) {
                    /**
                     * Previene la acción por defecto del enlace.
                     */
                    event.preventDefault();
                    /**
                     * Establece el valor del campo de nombre de usuario con la sugerencia.
                     */
                    document.getElementById('username').value = data.sugerencia;
                    /**
                     * Oculta el contenedor de sugerencias.
                     */
                    suggestionElement.style.display = 'none';
                });
            } else {
                /**
                 * Si es otro tipo de error, lo muestra en el contenedor general de errores.
                 */
                document.getElementById('general-error').innerText = data.error;
            }
        } else {
            /**
             * Si no hay error, redirige a la página de registro exitoso.
             */
            window.location.href = '/usuarios/registro_exitoso/';
        }
    })
    /**
     * Captura y maneja errores en la petición AJAX.
     */
    .catch(error => console.error('Error:', error));
});

/**
 * Esta función obtiene el valor de una cookie específica por su nombre.
 *
 * @param {string} name - El nombre de la cookie que se desea obtener.
 * @returns {string|null} El valor de la cookie o null si no se encuentra.
 */
function getCookie(name) {
    /**
     * Inicializa la variable para el valor de la cookie como null.
     */
    let cookieValue = null;
    /**
     * Verifica si existen cookies en el documento y si no están vacías.
     */
    if (document.cookie && document.cookie !== '') {
        /**
         * Divide la cadena de cookies en un array, separando cada cookie por el punto y coma.
         */
        const cookies = document.cookie.split(';');
        /**
         * Itera sobre cada cookie en el array.
         */
        for (let i = 0; i < cookies.length; i++) {
            /**
             * Elimina los espacios en blanco al principio y al final de la cookie.
             */
            const cookie = cookies[i].trim();
            /**
             * Verifica si la cookie comienza con el nombre buscado más el signo de igual.
             */
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                /**
                 * Si la cookie es la buscada, decodifica el valor (eliminando los caracteres de escape)
                 * y lo asigna a cookieValue.
                 */
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                /**
                 * Termina el bucle una vez que la cookie se encuentra.
                 */
                break;
            }
        }
    }
    /**
     * Retorna el valor de la cookie o null si no se encontró.
     */
    return cookieValue;
}

/**
 * Obtiene el elemento HTML donde se mostrarán los mensajes de error.
 */
const generalErrorDiv = document.getElementById('general-error');
/**
 * Obtiene el campo de nombre de usuario.
 */
const usernameInput = document.getElementById('username');
/**
 * Obtiene el campo de email.
 */
const emailInput = document.getElementById('email');
/**
 * Obtiene el campo de email2.
 */
const email2Input = document.getElementById('email2');
/**
 * Obtiene el campo de password.
 */
const passwordInput = document.getElementById('password');
/**
 * Obtiene el campo de password2.
 */
const password2Input = document.getElementById('password2');

/**
 * Agrega un listener al campo de nombre de usuario para borrar el mensaje de error cuando se ingrese texto.
 */
usernameInput.addEventListener('input', function() {
    generalErrorDiv.textContent = '';
});

/**
 * Agrega un listener al campo de email para borrar el mensaje de error cuando se ingrese texto.
 */
emailInput.addEventListener('input', function() {
    generalErrorDiv.textContent = '';
});

/**
 * Agrega un listener al campo de email2 para borrar el mensaje de error cuando se ingrese texto.
 */
email2Input.addEventListener('input', function() {
    generalErrorDiv.textContent = '';
});

/**
 * Agrega un listener al campo de password para borrar el mensaje de error cuando se ingrese texto.
 */
passwordInput.addEventListener('input', function() {
    generalErrorDiv.textContent = '';
});

/**
 * Agrega un listener al campo de password2 para borrar el mensaje de error cuando se ingrese texto.
 */
password2Input.addEventListener('input', function() {
    generalErrorDiv.textContent = '';
});
