document.querySelectorAll(".dropdown-btn").forEach(button => {
    button.addEventListener("click", () => {
        
        const dropdown = button.nextElementSibling;

        dropdown.style.display = 
            dropdown.style.display === "block" ? "none" : "block";

        button.querySelector(".arrow").classList.toggle("rotate");
    });
});

