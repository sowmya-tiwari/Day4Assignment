
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registerForm");

    if (form) {
        form.addEventListener("submit", function (event) {
            const name = document.getElementById("name").value.trim();
            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value;

            if (!name || !email || !password) {
                event.preventDefault();
                alert("Please fill in all fields.");
                return;
            }

            if (password.length < 6) {
                event.preventDefault();
                alert("Password must contain at least 6 characters.");
                return;
            }

            alert("Submitting registration form...");
        });
    }
});
