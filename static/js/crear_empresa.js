// JS específico para crear_empresa.html
// Lógica para mostrar el SweetAlert2 cuando la empresa es creada
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('crearEmpresaForm');
    const confirmarBtn = document.getElementById('confirmarCrearEmpresaBtn');
    if (form && confirmarBtn) {
        confirmarBtn.addEventListener('click', function(event) {
            event.preventDefault();
            // Busca el input cuyo name sea "nombre" (más robusto para Django forms)
            const nombreInput = form.querySelector('[name="nombre"]');
            const nombre = nombreInput ? nombreInput.value : '';
            Swal.fire({
                title: 'Confirmar Creación',
                html: `¿Está seguro de que desea crear la empresa <strong>${nombre}</strong>?`,
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#a86e17',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, crear',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    form.submit();
                }
            });
        });
    }
});
