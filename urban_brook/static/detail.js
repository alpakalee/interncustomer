document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('tr[data-href]').forEach(row => {
        row.addEventListener('click', function() {
            const url = row.dataset.href;
            window.open(url, '_blank');
        });
    });
});
