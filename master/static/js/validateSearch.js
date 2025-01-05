function validateSearch() {
    const searchInput = document.getElementById('search').value.trim();
    const errorMessage = document.getElementById('error-message');

    if (searchInput === '') {
        errorMessage.style.display = 'block'; 
        return false;
    } else {
        errorMessage.style.display = 'none'; 
        return true;
    }
}