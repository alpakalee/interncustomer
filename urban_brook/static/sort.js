document.addEventListener('DOMContentLoaded', function() {
    const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

    const parseDate = (dateStr) => {
        // 날짜 형식을 "yy년mm월dd일" 형식으로 가정하고 파싱합니다.
        const parts = dateStr.match(/(\d{2})년(\d{2})월(\d{2})일/);
        if (parts) {
            const year = 2000 + parseInt(parts[1]); // 2000년대 이후를 가정
            const month = parseInt(parts[2]) - 1;
            const day = parseInt(parts[3]);
            return new Date(year, month, day);
        }
        return new Date(); // 유효하지 않은 날짜 형식의 경우 현재 날짜 반환
    };

    const comparer = (idx, asc) => (a, b) => {
        const v1 = getCellValue(a, idx);
        const v2 = getCellValue(b, idx);
        
        // 0번째 열(상담일)과 2번째 열(행사날짜)에 대해서는 날짜 형식으로 처리
        if (idx === 0 || idx === 2) {
            return (asc ? 1 : -1) * (parseDate(v1) - parseDate(v2));
        }
        
        // 숫자 비교
        if (!isNaN(v1) && !isNaN(v2)) {
            return (asc ? 1 : -1) * (v1 - v2);
        }
        
        // 문자열 비교
        return (asc ? 1 : -1) * v1.toString().localeCompare(v2);
    };

    document.querySelectorAll('th').forEach((th, index) => {
        if (![3, 4, 5].includes(index)) { // 3(시간), 4(예약자), 5(연락처) 에 대한 정렬 제외
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
