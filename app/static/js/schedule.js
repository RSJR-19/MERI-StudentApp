const blurOverlay = document.getElementById("blurOverlay");
const fileUpload = document.getElementById("fileUpload");
const confirmBtn = document.getElementById("confirmBtn");
const cancelBtn = document.getElementById("cancelBtn");
const privacyAgreement = document.getElementById("privacyAgreement");

blurOverlay.style.display = "none";

let accepted = false;

fileUpload.addEventListener('click', (e)=>{
    accepted = false;
    privacyAgreement.checked = false;
    e.preventDefault();
    blurOverlay.style.display = "flex";
    setTimeout(()=>{
        blurOverlay.classList.add("reveal");
    }, 100)

});

confirmBtn.addEventListener('click', ()=>{
    if (!accepted){
        alert("Please check the privacy agreement checkbox first before proceeding.");
    }
    else if (accepted){
        alert("done")
    }
})

cancelBtn.addEventListener('click', ()=>{
    blurOverlay.classList.remove("reveal");
    setTimeout(()=>{
        blurOverlay.style.display = "none";
    }, 500);
    confirmBtn.classList.remove('clickable');
});

privacyAgreement.addEventListener('click', ()=>{
    if (!accepted){
        accepted = true;
        confirmBtn.classList.add("clickable");
    }
    else{
        accepted = false;
        confirmBtn.classList.remove('clickable');
    }
})