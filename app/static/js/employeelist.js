
document.querySelectorAll(".edit-btn").forEach(btn => {
    btn.addEventListener("click", function (e) {
        e.preventDefault();

        let employeeId = this.dataset.id;

        // Fetch employee data from server
        fetch(`/get_employee/${employeeId}`)
            .then(res => res.json())
            .then(data => {
                // Populate form fields with employee data
                document.getElementById("emp_id").value = data.id;
                document.getElementById("emp_store").value = data.store_id || "";
                document.getElementById("emp_name").value = data.employee_name || "";
                document.getElementById("emp_email").value = data.email || "";
                document.getElementById("emp_designation").value = data.designation || "";
                document.getElementById("emp_status").value = data.status || "Active";
                document.getElementById("emp_address_name").value = data.address_name || "";
                document.getElementById("emp_street").value = data.street_name || "";
                document.getElementById("emp_town").value = data.town || "";
                document.getElementById("emp_locality").value = data.locality || "";
                document.getElementById("emp_post_code").value = data.post_code || "";
                document.getElementById("emp_contact1").value = data.contact1 || "";
                document.getElementById("emp_contact2").value = data.contact2 || "";

                // Show modal
                document.getElementById("editEmpModal").style.display = "flex";
            })
            .catch(error => {
                console.error("Error fetching employee data:", error);
                alert("Error loading employee data. Please try again.");
            });
    });
});

document.getElementById("empCloseBtn").onclick =
document.getElementById("empCancelBtn").onclick = function () {
    document.getElementById("editEmpModal").style.display = "none";
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

