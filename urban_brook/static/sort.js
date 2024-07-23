document.addEventListener('DOMContentLoaded', function() {
    const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

    const comparer = (idx, asc) => (a, b) => ((v1, v2) =>
        v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
    )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

    document.querySelectorAll('th').forEach((th, index) => {
        if (![3, 4, 5].includes(index)) {
            th.addEventListener('click', function() {
                const table = th.closest('table');
                const sortIcon = th.querySelector('.sort-icon');
                const isAsc = sortIcon.dataset.sort === 'asc';
                sortIcon.src = isAsc ? 'static/up.png' : 'static/down.png';
                sortIcon.dataset.sort = isAsc ? 'desc' : 'asc';

                Array.from(table.querySelectorAll('tbody tr'))
                    .sort(comparer(index, !isAsc))
                    .forEach(tr => table.querySelector('tbody').appendChild(tr));
            });
        }
    });
});
