// mensajes_confirmacion_administracion_usuarios.js

// Función para mostrar un modal de confirmación personalizado usando SweetAlert2
function mostrarConfirmacion(event, action) {
    event.preventDefault(); // Detiene el envío del formulario inmediatamente

    let titulo = "Confirmar Acción";
    let mensaje = "";
    let icon = "question"; // Icono por defecto

    if (action === 'cambiar_rol') {
        mensaje = "¿Estás seguro de que quieres cambiar el rol de este usuario?";
        icon = "question";
    } else if (action === 'archivar') {
        mensaje = "¿Estás seguro de que quieres archivar este usuario? Se desactivará automáticamente.";
        icon = "warning"; // Icono de advertencia para archivar
    } else if (action === 'activar') {
        mensaje = "¿Estás seguro de que quieres activar este usuario?";
        icon = "question";
    } else if (action === 'desactivar') {
        mensaje = "¿Estás seguro de que quieres desactivar este usuario?";
        icon = "warning"; // Icono de advertencia para desactivar
    } else {
        // Mensaje por defecto si la acción no es reconocida
        mensaje = "¿Estás seguro de realizar esta acción?";
    }

    // Mostrar el modal de SweetAlert2
    Swal.fire({
        title: titulo,
        text: mensaje,
        icon: icon,
        showCancelButton: true,
        confirmButtonColor: '#3085d6', // Color para el botón de confirmar
        cancelButtonColor: '#d33',    // Color para el botón de cancelar
        confirmButtonText: 'Sí, continuar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        // Si el usuario hizo clic en "Sí, continuar"
        if (result.isConfirmed) {
            // Obtén el formulario asociado al evento
            const form = event.target.closest('form');
            if (form) {
                // Añade un campo oculto para indicar que la confirmación ha pasado por JS
                // Esto puede ser útil si necesitas verificar en el backend
                const confirmedInput = document.createElement('input');
                confirmedInput.type = 'hidden';
                confirmedInput.name = 'confirmed_by_js';
                confirmedInput.value = 'true';
                form.appendChild(confirmedInput);

                // Envía el formulario programáticamente
                form.submit();
            }
        }
    });
}

// Eliminamos la vieja función confirmarAccion si ya no se usará directamente en onsubmit
// function confirmarAccion(action) { ... }