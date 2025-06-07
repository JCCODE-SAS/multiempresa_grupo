// JS específico para panel_administrativo.html
// Solo maneja el logout seguro (el resto de la navbar lo maneja navbar.js)
document.addEventListener('DOMContentLoaded', function() {
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(event) {
            event.preventDefault();
            document.getElementById('logoutForm').submit();
        });
    }
});
