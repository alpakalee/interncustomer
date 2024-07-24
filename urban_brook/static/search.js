document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const tableRows = document.querySelectorAll('#customer-table tbody tr');

    searchInput.addEventListener('keyup', function() {
        const filter = searchInput.value.toLowerCase();

        tableRows.forEach(row => {
<<<<<<< HEAD
            const event_type = row.children[1].innerText.toLowerCase();
=======
            const event_type = row.children[2].innerText.toLowerCase();
>>>>>>> 31aa8f284e689c6b5d15f596eaaf7aca01994cdf
            const customerName = row.children[4].innerText.toLowerCase();
            const phoneNumber = row.children[5].innerText.toLowerCase();

            if (customerName.includes(filter) || phoneNumber.includes(filter) || event_type.includes(filter)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
});
