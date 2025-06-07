// JS para editar_usuario.html
// Puedes agregar aquí validaciones, mensajes o lógica personalizada para el formulario de edición de usuario.
// Ejemplo: mostrar mensaje de éxito o error tras guardar cambios.

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            Swal.fire({
                title: 'Confirmar Edición',
                text: '¿Estás seguro de que deseas guardar los cambios de este usuario?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#a86e17',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, guardar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    form.submit();
                }
            });
        });
    }
});
