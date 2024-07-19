document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('toggle-dark-mode');
    const body = document.body;
    const toggleIcon = toggleButton.querySelector('.toggle-icon');

    // Verifica si el modo oscuro está almacenado en el almacenamiento local
    if (localStorage.getItem('dark-mode') === 'enabled') {
        body.classList.add('dark-mode');
        toggleIcon.classList.remove('sun');
        toggleIcon.classList.add('moon');
    } else {
        body.classList.add('light-mode');
        toggleIcon.classList.remove('moon');
        toggleIcon.classList.add('sun');
    }

    // Añade un listener para el botón
    toggleButton.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
        body.classList.toggle('light-mode');

        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('dark-mode', 'enabled');
            toggleIcon.classList.remove('sun');
            toggleIcon.classList.add('moon');
        } else {
            localStorage.setItem('dark-mode', 'disabled');
            toggleIcon.classList.remove('moon');
            toggleIcon.classList.add('sun');
        }
    });
});
