function resetSearch(event, dynamicUrl) {
    event.preventDefault(); // Prevent the form from submitting

    // Clear the search field
    var form = event.target.closest('form');
    var searchField = form.querySelector('input[name^="search_"]');
    if (searchField) {
      searchField.value = '';
    }

    // Submit the form
    form.action = dynamicUrl;
    form.submit();
}