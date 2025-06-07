// JS específico para editar_empresa.html
// Unifica el modal de confirmación usando SweetAlert2 (igual que editar_usuario.js)

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('editarEmpresaForm');
    const confirmarCambiosBtn = document.getElementById('confirmarCambiosBtn');
    if (form && confirmarCambiosBtn) {
        confirmarCambiosBtn.addEventListener('click', function(event) {
            event.preventDefault();
            const nombre = document.getElementById('nombre').value;
            Swal.fire({
                title: 'Confirmar Edición',
                html: `¿Está seguro de que desea guardar los cambios para la empresa <strong>${nombre}</strong>?`,
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
