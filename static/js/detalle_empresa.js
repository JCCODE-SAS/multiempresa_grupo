// JS específico para detalle_empresa.html
// Lógica para el botón de logout

document.addEventListener('DOMContentLoaded', function() {
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(event) {
            event.preventDefault();
            document.getElementById('logoutForm').submit();
        });
    }
});
