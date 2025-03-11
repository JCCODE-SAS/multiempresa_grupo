// javascript para recuperar contraseña
document.getElementById('recuperarForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita que se recargue la página
    const email = document.getElementById('email').value; // Obtiene el valor del campo email
    const confirmEmail = document.getElementById('confirmEmail').value; // Obtiene el valor del campo confirmEmail
    // Realiza una petición POST al servidor con los datos del formulario
    fetch('{% url "usuarios:recuperar_contrasena" %}', { // URL de la vista
        method: 'POST', // Método POST
        headers: { // Cabeceras de la petición
            'Content-Type': 'application/json', // La petición envía un JSON
            'X-CSRFToken': '{{ csrf_token }}' // Se añade el token CSRF
        },
        body: JSON.stringify({ email: email, confirmEmail: confirmEmail })
    })  // Se convierte la respuesta a JSON
    .then(response => response.json())  // Se obtiene el JSON
    .then(data => {     
        const mensajeDiv = document.getElementById('mensaje');
        if (data.message) { // Si hay un mensaje
            mensajeDiv.textContent = data.message;
            mensajeDiv.className = 'mt-3 text-center text-success';  // Se muestra el mensaje
        } else { // Si hay un error se muestra el mensaje de error
            mensajeDiv.textContent = data.error;
            mensajeDiv.className = 'mt-3 text-center text-danger';
        }
    });
});