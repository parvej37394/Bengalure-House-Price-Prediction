document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("predictionForm");

    if (form) {
        form.addEventListener("submit", function (event) {
            const location = document.getElementById("location").value;
            const bhk = document.getElementById("bhk").value;
            const bath = document.getElementById("bath").value;
            const totalSqft = document.getElementById("total_sqft").value;

            // Simple Client-Side Validation
            if (!location || !bhk || !bath || !totalSqft) {
                alert("Please fill in all fields before submitting.");
                event.preventDefault(); // Prevents form submission
                return;
            }

            if (bhk <= 0 || bath <= 0 || totalSqft <= 0) {
                alert("Please enter positive numeric values for BHK, Bathrooms, and Square Feet.");
                event.preventDefault();
                return;
            }
        });
    }
});