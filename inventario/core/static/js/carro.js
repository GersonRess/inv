document.addEventListener('DOMContentLoaded', function() {
    const cartForm = document.getElementById('cart-form');
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');

    // Función para actualizar el total del carrito
    function updateCartTotal() {
        let total = 0;
        cartItems.querySelectorAll('tr').forEach(function(row) {
            const price = parseFloat(row.querySelector('.price').textContent.replace('$', ''));
            const quantity = parseInt(row.querySelector('.quantity-input').value, 10);
            const totalCell = row.querySelector('.total');
            const rowTotal = price * quantity;
            totalCell.textContent = `$${rowTotal.toFixed(2)}`;
            total += rowTotal;
        });
        cartTotal.textContent = `$${total.toFixed(2)}`;
    }

    // Event listener para los cambios en las cantidades
    cartItems.addEventListener('input', function(event) {
        if (event.target.classList.contains('quantity-input')) {
            updateCartTotal();
        }
    });

    // Inicializa el total del carrito al cargar la página
    updateCartTotal();
});