const blurOverlay = document.getElementById("blurOverlay");
const fileUpload = document.getElementById("fileUpload");
const confirmBtn = document.getElementById("confirmBtn");
const cancelBtn = document.getElementById("cancelBtn");
const privacyAgreement = document.getElementById("privacyAgreement");
const extractingScreen = document.getElementById("extractingScreen");

blurOverlay.style.display = "none";
extractingScreen.style.display = "none";

let accepted = false;
let allowFilePicker = false;

fileUpload.addEventListener("click", (e) => {
    if (allowFilePicker) {
        allowFilePicker = false;
        return;
    }
    e.preventDefault();

    privacyAgreement.checked = false;
    accepted = false;

    blurOverlay.style.display = "flex";
    setTimeout(() => {
        blurOverlay.classList.add("reveal");
    }, 100);
});

confirmBtn.addEventListener("click", () => {
    if (!accepted) {
        alert("Please check the privacy agreement checkbox first before proceeding.");
        return;
    }

    blurOverlay.classList.remove("reveal");

    setTimeout(() => {
        blurOverlay.style.display = "none";
        allowFilePicker = true;
        fileUpload.click();
    }, 500);
});

cancelBtn.addEventListener("click", () => {
    blurOverlay.classList.remove("reveal");

    setTimeout(() => {
        blurOverlay.style.display = "none";
    }, 500);

    confirmBtn.classList.remove("clickable");
});


privacyAgreement.addEventListener("change", () => {
    accepted = privacyAgreement.checked;

    confirmBtn.classList.toggle("clickable", accepted);
});

fileUpload.addEventListener("change", async () => {
    const file = fileUpload.files[0];

    if (!file) {
        return;
    }

    const formData = new FormData();
    formData.append("eaf", file);

    try {
        confirmBtn.disabled = true;
        const csrfToken = document
        .querySelector('meta[name="csrf-token"]')
        .getAttribute("content");

        const response = await fetch("/extract-eaf", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        },
        body: formData
        });

        const responseText = await response.text();

        let result;

        try {
        result = JSON.parse(responseText);
        } catch {
        console.error("Server returned a non-JSON response:", responseText);
        throw new Error("The server returned an unexpected response.");
        }
        
        if (!response.ok || !result.success) {
            alert(result.message || "Unable to extract EAF.");
            return;
        }

        console.log("Extracted EAF Text:");
        console.log(result.extracted_text);

        alert("EAF text extracted successfully!");

    } catch (error) {

        console.error("EAF Upload Error:", error);
        alert("Something went wrong while processing your EAF.");

    } finally {
        confirmBtn.disabled = false;
        fileUpload.value = "";
    }
});

