const passwordInput = document.getElementById("passwordInput");

const confirmPasswordInput = document.getElementById("confirmPasswordInput");

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