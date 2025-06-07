// navbar.js: JS para la navbar de administración (logout y fecha/hora en tiempo real)

document.addEventListener('DOMContentLoaded', function() {
    // Logout seguro
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(event) {
            event.preventDefault();
            document.getElementById('logoutForm').submit();
        });
    }
    // Fecha y hora en tiempo real
    function actualizarFechaHoraNavbar() {
        const fechaElem = document.getElementById('fecha-actual');
        const horaElem = document.getElementById('hora-actual');
        if (!fechaElem || !horaElem) return;
        const ahora = new Date();
        const fecha = ahora.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' });
        const hora = ahora.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        fechaElem.textContent = fecha;
        horaElem.textContent = hora;
    }
    setInterval(actualizarFechaHoraNavbar, 1000);
    actualizarFechaHoraNavbar();
});
