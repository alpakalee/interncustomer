document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const tableRows = document.querySelectorAll('#customer-table tbody tr');

    searchInput.addEventListener('keyup', function() {
        const filter = searchInput.value.toLowerCase();

        tableRows.forEach(row => {
            const customerName = row.children[2].innerText.toLowerCase();
            const phoneNumber = row.children[4].innerText.toLowerCase();

            if (customerName.includes(filter) || phoneNumber.includes(filter)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
});
