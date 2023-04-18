const table = document.getElementById('runs-table');
const tbody = table.querySelector('tbody');
const rows = tbody.querySelectorAll('tr');
const maxRows = 10; // Maximum number of rows to show

function get_token() {
    return $('input[name="csrfmiddlewaretoken"]').val();
}

if (rows.length > maxRows) {
    // Hide rows that exceed the maximum number
    for (let i = maxRows; i < rows.length; i++) {
        rows[i].style.display = 'none';
    }

    // Add a "show more" button
    const showMoreBtn = document.createElement('button');
    showMoreBtn.innerText = 'Show more';
    showMoreBtn.classList.add('btn');
    showMoreBtn.classList.add('btn-dark');
    showMoreBtn.classList.add('centered'); // Add a new class to the button
    showMoreBtn.addEventListener('click', () => {
        for (let i = maxRows; i < rows.length; i++) {
            rows[i].style.display = '';
        }
        showMoreBtn.style.display = 'none';
    });

    // Add the button to the container
    const container = table.parentNode;
    container.insertBefore(showMoreBtn, table.nextSibling);
}
