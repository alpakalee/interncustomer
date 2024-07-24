document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const tableRows = document.querySelectorAll('#customer-table tbody tr');

    searchInput.addEventListener('keyup', function() {
        const filter = searchInput.value.toLowerCase();

        tableRows.forEach(row => {
            const event_type = row.children[1].innerText.toLowerCase(); //행사 구분
            const customerName = row.children[4].innerText.toLowerCase(); // 예약자명
            const phoneNumber = row.children[5].innerText.toLowerCase(); // 전화번호

            if (customerName.includes(filter) || phoneNumber.includes(filter) || event_type.includes(filter)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
});
