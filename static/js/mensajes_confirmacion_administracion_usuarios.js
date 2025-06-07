// mensajes_confirmacion_administracion_usuarios.js

// Función para mostrar un modal de confirmación personalizado usando SweetAlert2
function mostrarConfirmacion(event, action) {
    event.preventDefault(); // Detiene el envío del formulario inmediatamente

    let titulo = "Confirmar Acción";
    let mensaje = "";
    let icon = "question";

    // === Lógica para definir el mensaje y el icono según la acción ===
    if (action === 'cambiar_rol') {
        mensaje = "¿Estás seguro de que quieres cambiar el rol de este usuario?";
        icon = "question";
    } else if (action === 'archivar') {
        mensaje = "¿Estás seguro de que quieres archivar este usuario? Se desactivará automáticamente.";
        icon = "warning";
    } else if (action === 'activar') {
        mensaje = "¿Estás seguro de que quieres activar este usuario?";
        icon = "question";
    } else if (action === 'desactivar') {
        mensaje = "¿Estás seguro de que quieres desactivar este usuario?";
        icon = "warning";
    } else {
        // Mensaje por defecto si la acción no es reconocida
        mensaje = "¿Estás seguro de realizar esta acción?";
    }
    // === Fin lógica para definir el mensaje y el icono ===


    // Mostrar el modal de SweetAlert2
    Swal.fire({
        title: titulo,
        text: mensaje,
        icon: icon,
        showCancelButton: true,
        confirmButtonColor: '#a86e17',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, continuar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        // Si el usuario hizo clic en "Sí, continuar"
        if (result.isConfirmed) {
            const form = event.target.closest('form'); // Obtén el formulario asociado al evento

            if (form) {
                // === Añade un campo oculto para el parámetro 'action' ===
                const actionInput = document.createElement('input');
                actionInput.type = 'hidden';
                actionInput.name = 'action'; // El nombre del parámetro esperado en la vista de Django
                actionInput.value = action;  // El valor es el tipo de acción que pasamos ('cambiar_rol', etc.)
                form.appendChild(actionInput);
                // === Fin añadir campo 'action' ===

                // === Añade el campo oculto para indicar que la confirmación ha pasado por JS (opcional pero bueno para backend check) ===
                const confirmedInput = document.createElement('input');
                confirmedInput.type = 'hidden';
                confirmedInput.name = 'confirmed_by_js';
                confirmedInput.value = 'true';
                form.appendChild(confirmedInput);
                // === Fin añadir campo 'confirmed_by_js' ===


                // Envía el formulario programáticamente
                form.submit();
            }
        }
    });
}

// Eliminamos la vieja función confirmarAccion si ya no se usará directamente en onsubmit
// function confirmarAccion(action) { ... }