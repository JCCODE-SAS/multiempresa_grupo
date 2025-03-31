function confirmarAccion(action) {
    console.log("Acción:", action); // Agrega esta línea
    let mensaje = "";
    if (action === 'cambiar_rol') {
        mensaje = "¿Estás seguro de que quieres cambiar el rol de este usuario?";
    } else if (action === 'archivar') {
        mensaje = "¿Estás seguro de que quieres archivar este usuario?";
    } else if (action === 'activar') {
        mensaje = "¿Estás seguro de que quieres activar este usuario?";
    } else if (action === 'desactivar') {
        mensaje = "¿Estás seguro de que quieres desactivar este usuario?";
    }
    return confirm(mensaje);
}