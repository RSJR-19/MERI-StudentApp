const passwordInput = document.getElementById("passwordInput");
const confirmPasswordInput = document.getElementById("confirmPasswordInput");
const currentDate = document.getElementById("currentDate");
const currentDay = document.getElementById("currentDay");
const overlayScreeen = document.getElementById("overlayScreen");
const hamburgerBtn = document.getElementById("hamburgerBtn");
const sideBarContainer = document.getElementById("sideBarContainer");
const backBtn = document.getElementById("backBtn");
const notYetBtn = document.getElementById("notYetBtn");
const yesSirBtn = document.getElementById("yesSirBtn");
const logoutBtn = document.getElementById("logoutBtn");
const logoutConfirmOverlay = document.getElementById("logoutConfirmOverlay");
const logoutConfirm = document.getElementById("logoutConfirm");

overlayScreeen.style.display = "none";
logoutConfirmOverlay.style.display = "none";

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

hamburgerBtn.addEventListener('click', ()=>{
    overlayScreeen.style.display = "flex";
    setTimeout(()=>{
        overlayScreeen.classList.add("reveal");
        setTimeout(()=>{
            sideBarContainer.classList.add("show");
        }, 400)
    }, 100)
});

backBtn.addEventListener('click', ()=>{
    sideBarContainer.classList.remove("show");
    setTimeout(()=>{
        overlayScreeen.classList.remove("reveal");
        setTimeout(()=>{
            overlayScreeen.style.display = "none";
        }, 500)
    }, 300);
});

logoutBtn.addEventListener('click', ()=>{
    logoutConfirmOverlay.style.display = "flex";
    setTimeout(()=>{
        logoutConfirmOverlay.classList.add("reveal");
        setTimeout(()=>{
            logoutConfirm.classList.add("show");
        }, 100)
    }, 100)
});

notYetBtn.addEventListener('click', ()=>{
    logoutConfirm.classList.remove("show");
    setTimeout(()=>{
    logoutConfirmOverlay.classList.remove("reveal");
    setTimeout(()=>{
        logoutConfirmOverlay.style.display = "none";
    }, 300)
})});
