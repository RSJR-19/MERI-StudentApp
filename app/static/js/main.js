const passwordInput = document.getElementById("passwordInput");
const confirmPasswordInput = document.getElementById("confirmPasswordInput");
const currentDate = document.getElementById("currentDate");
const currentDay = document.getElementById("currentDay");

if (passwordInput && confirmPasswordInput) {
    function checkPasswordMatch() {
        if (confirmPasswordInput.value !== passwordInput.value) {
            confirmPasswordInput.setCustomValidity("Passwords do not match.");
        } else {
            confirmPasswordInput.setCustomValidity("");
        }
    }
    passwordInput.addEventListener("input", checkPasswordMatch);

    confirmPasswordInput.addEventListener("input", checkPasswordMatch);
}

if (currentDate && currentDay) {
    const today = new Date();

    currentDate.textContent = today.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric"
    });

    currentDay.textContent = today.toLocaleDateString("en-US", {
        weekday: "long"
    });
}