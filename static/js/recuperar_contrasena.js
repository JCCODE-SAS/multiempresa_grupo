// javascript para recuperar contraseña
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recuperarForm');
    const mensajeDiv = document.getElementById('mensaje');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Evita que el formulario se envíe de la manera tradicional

        const email = document.getElementById('email').value;
        const confirmEmail = document.getElementById('confirmEmail').value;

        fetch(recuperarUrl, { // Usa la variable recuperarUrl que se define en la plantilla HTML
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Asegúrate de tener esta función o similar
            },
            body: JSON.stringify({ email: email, confirmEmail: confirmEmail })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err; }); // Lanza el error con el detalle
            }
            return response.json();
        })
        .then(data => {
            mensajeDiv.textContent = data.message;
            mensajeDiv.classList.add('text-success');
            mensajeDiv.classList.remove('text-danger');
            form.reset(); // Resetear el formulario despues de mostrar el mensaje
        })
        .catch(error => {
            console.error('Error:', error);
            mensajeDiv.textContent = error.error || 'Hubo un error al enviar el correo de recuperación.';
            mensajeDiv.classList.add('text-danger');
            mensajeDiv.classList.remove('text-success');
        });
    });

    // Función para obtener la cookie CSRF (si no la tienes ya)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
