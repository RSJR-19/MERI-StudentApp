window.addEventListener('load', ()=>{
    const blurOverlay = document.getElementById("blurOverlay");
    const addExpenseBtn = document.getElementById("addExpenseBtn");
    const addExpenseScreen = document.getElementById("addExpenseScreen");
    const updateExpenseScreen = document.getElementById("updateExpenseScreen");
    const updateBudgetScreen = document.getElementById("updateBudgetScreen");
    const updateBudgetBtn = document.getElementById("updateBudgetBtn");
    const classExpenseItems = document.querySelectorAll(".expense-item");
    const cancelBtnAdd = document.getElementById("cancelBtnAdd");
    const saveChangesBtn = document.getElementById("saveChangesBtn");
    const updateCancel = document.getElementById("updateCancel");
    const deleteBlurOverlay = document.getElementById("deleteBlurOverlay");
    const deleteConfirm = document.getElementById("deleteConfirm");
    const notYetBtn = document.getElementById("notYetBtn");

    blurOverlay.style.display = "none";
    deleteBlurOverlay.style.display = "none";

    addExpenseBtn.addEventListener('click', ()=>{
        blurOverlay.style.display = "flex";
        addExpenseScreen.style.display = "flex";
        setTimeout(()=>{
            blurOverlay.classList.add("reveal");
        }, 100); 
    });

    updateBudgetBtn.addEventListener('click', ()=>{
        blurOverlay.style.display = "flex";
        updateBudgetScreen.style.display = "flex";
        setTimeout(()=>{
            blurOverlay.classList.add("reveal");
        }, 100); 
    });

    classExpenseItems.forEach(classExpenseItem =>{
        classExpenseItem.addEventListener("click", ()=>{
        blurOverlay.style.display = "flex";
        updateExpenseScreen.style.display = "flex";
        setTimeout(()=>{
            blurOverlay.classList.add("reveal");
        }, 100); 
        });
    });

    cancelBtnAdd.addEventListener('click', ()=>{
        blurOverlay.classList.remove("reveal");
        setTimeout(()=>{
            blurOverlay.style.display = "none";
            addExpenseScreen.style.display = "none";
        }, 500)
    });

    saveChangesBtn.addEventListener('click', ()=>{
        blurOverlay.classList.remove("reveal");
        setTimeout(()=>{
            blurOverlay.style.display = "none";
            updateExpenseScreen.style.display = "none";
        }, 500) 
    });

    updateCancel.addEventListener('click', ()=>{
        blurOverlay.classList.remove("reveal");
        setTimeout(()=>{
            blurOverlay.style.display = "none";
            updateBudgetScreen.style.display = "none";
        }, 500)
    });

    deleteExpenseBtn.addEventListener('click',()=>{
        deleteBlurOverlay.style.display = "flex";
        setTimeout(()=>{
            deleteConfirm.classList.add("show");
        }, 100)
    })

    notYetBtn.addEventListener('click', ()=>{
        deleteConfirm.classList.remove("show");
        setTimeout(()=>{
            deleteBlurOverlay.style.display = "none";
        }, 250);
    })

});