document.querySelectorAll(".edit-btn").forEach(btn => {
    btn.addEventListener("click", function () {

        let storeId = this.dataset.id;

        fetch(`/get_store/${storeId}`)
            .then(res => res.json())
            .then(data => {

                document.getElementById("edit_id").value = data.id;
                document.getElementById("edit_store_name").value = data.store_name;
                document.getElementById("edit_email").value = data.email;
                document.getElementById("edit_address_name").value = data.address_name;
                document.getElementById("edit_street_name").value = data.street_name;
                document.getElementById("edit_town").value = data.town;
                document.getElementById("edit_locality").value = data.locality;
                document.getElementById("edit_post_code").value = data.post_code;
                document.getElementById("edit_contact1").value = data.contact1;
                document.getElementById("edit_contact2").value = data.contact2;

                // Show modal
                document.getElementById("editModal").style.display = "flex";
            });
    });
});

document.getElementById("closeModal").addEventListener("click", function () {
    document.getElementById("editModal").style.display = "none";
});
document.getElementById("closeModalBtn").onclick =
document.getElementById("closeModal").onclick = function () {
    document.getElementById("editModal").style.display = "none";
};

// for filter
let filterTimeout;

// Debounced filter submission for text inputs - increased delay for better typing experience
document.querySelectorAll('.filters input[type="text"]').forEach(input => {
    input.addEventListener('input', () => {
        clearTimeout(filterTimeout);
        filterTimeout = setTimeout(() => {
            document.getElementById('filterForm').submit();
        }, 1500); // Wait 1.5 seconds after user stops typing to allow complete words
    });
    
    // Also submit on Enter key press
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            clearTimeout(filterTimeout);
            e.preventDefault();
            document.getElementById('filterForm').submit();
        }
    });
    
    // Submit on blur (when user clicks away from input)
    input.addEventListener('blur', () => {
        clearTimeout(filterTimeout);
        // Small delay to allow clicking the filter button
        setTimeout(() => {
            document.getElementById('filterForm').submit();
        }, 200);
    });
});

// Immediate submission for date changes
const dateInput = document.getElementById('date');
if (dateInput) {
    dateInput.addEventListener('change', () => {
        clearTimeout(filterTimeout);
        document.getElementById('filterForm').submit();
    });
}

// Handle form submission
const filterForm = document.getElementById('filterForm');
if (filterForm) {
    filterForm.addEventListener('submit', function(e) {
        // Clear any pending timeouts when form is manually submitted
        clearTimeout(filterTimeout);
        // Form will submit normally via POST
    });
}