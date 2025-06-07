// JS específico para administracion_usuarios.html

document.addEventListener('DOMContentLoaded', function() {
    // Código para el logout
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(event) {
            event.preventDefault();
            document.getElementById('logoutForm').submit();
        });
    }

    // === Nuevo código para los formularios de acción de usuario ===
    // Selecciona todos los formularios dentro de las celdas de acciones (<td> con clase action-buttons)
    const actionForms = document.querySelectorAll('td.action-buttons form');
    actionForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            // Obtiene el tipo de acción del atributo data-action-type del formulario
            const actionType = this.getAttribute('data-action-type');
            // Llama a la función de SweetAlert2
            if (typeof mostrarConfirmacion === 'function') {
                mostrarConfirmacion(event, actionType);
            }
        });
    });
    // === Fin nuevo código ===
});
