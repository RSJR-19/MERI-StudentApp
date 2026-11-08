window.addEventListener("DOMContentLoaded", () => {
    const blurOverlay = document.getElementById("blurOverlay");
    const addBudgetState = document.getElementById("addBudgetState");
    const updateBudgetBtn = document.getElementById("updateBudgetBtn");
    const addExpenseBtn = document.getElementById("addExpenseBtn");
    const addExpenseScreen = document.getElementById("addExpenseScreen");
    const updateExpenseScreen = document.getElementById("updateExpenseScreen");
    const updateBudgetScreen = document.getElementById("updateBudgetScreen");
    const cancelBtnAdd = document.getElementById("cancelBtnAdd");
    const saveChangesBtn = document.getElementById("saveChangesBtn");
    const updateCancel = document.getElementById("updateCancel");
    const addExpenseConfirm = document.getElementById("addExpenseConfirm");
    const deleteExpenseBtn = document.getElementById("deleteExpenseBtn");
    const confirmBudgetUpdate = document.getElementById("confirmBudgetUpdate");
    const expenseTitleInput = document.getElementById("expenseTitleInput");
    const expenseAmountInput = document.getElementById("expenseAmountInput");
    const expenseDetailsInput = document.getElementById("expenseDetailsInput");
    const editExpenseTitle = document.getElementById("editExpenseTitle");
    const editExpenseAmount = document.getElementById("editExpenseAmount");
    const editExpenseDetails = document.getElementById("editExpenseDetails");
    const budgetAmountInput = document.getElementById("budgetAmountInput");
    const updateTitle = document.getElementById("updateTitle");
    const deleteBlurOverlay = document.getElementById("deleteBlurOverlay");
    const deleteConfirm = document.getElementById("deleteConfirm");
    const notYetBtn = document.getElementById("notYetBtn");
    const yesSirBtn = document.getElementById("yesSirBtn");

    let selectedExpenseId = null;

    let budgetMode = "create";

    blurOverlay.style.display = "none";
    deleteBlurOverlay.style.display = "none";

    const screens = [
        addExpenseScreen,
        updateExpenseScreen,
        updateBudgetScreen
    ];

    function hideAllScreens() {
        screens.forEach(screen => {
            screen.style.display = "none";
        });
    }
    hideAllScreens();

    function openScreen(screen) {
        hideAllScreens();
        blurOverlay.style.display = "flex";
        screen.style.display = "flex";
        setTimeout(() => {
            blurOverlay.classList.add("reveal");
        }, 100);
    }


    function closeScreen(screen) {
        blurOverlay.classList.remove("reveal");
        setTimeout(() => {
            blurOverlay.style.display = "none";
            screen.style.display = "none";
        }, 500);
    }

    if (addBudgetState) {
        addBudgetState.addEventListener("click", () => {
            budgetMode = "create";
            updateTitle.textContent = "SET DAILY BUDGET";
            confirmBudgetUpdate.textContent = "Set Budget";
            budgetAmountInput.value = "";
            openScreen(updateBudgetScreen);
        });

    }


    if (updateBudgetBtn) {
        updateBudgetBtn.addEventListener("click", () => {
            budgetMode = "update";

            updateTitle.textContent = "UPDATE BUDGET";
            confirmBudgetUpdate.textContent = "Update Budget";

            const totalBudget = document.getElementById("totalBudget");

            if (totalBudget) {
                budgetAmountInput.value =
                    totalBudget.textContent.replace(/[₱,\s]|total/g, "");
            }
            openScreen(updateBudgetScreen);

        });

    }
    if (addExpenseBtn) {

        addExpenseBtn.addEventListener("click", () => {

            expenseTitleInput.value = "";
            expenseAmountInput.value = "";
            expenseDetailsInput.value = "";
            openScreen(addExpenseScreen);

        });

    }

    document.addEventListener("click", (event) => {

        const expenseItem = event.target.closest(".expense-item");

        if (!expenseItem) return;

        selectedExpenseId = expenseItem.dataset.id;

        editExpenseTitle.value = expenseItem.dataset.title;
        editExpenseAmount.value = expenseItem.dataset.amount;
        editExpenseDetails.value = expenseItem.dataset.details;

        openScreen(updateExpenseScreen);

    });

    cancelBtnAdd.addEventListener("click", () => {
        closeScreen(addExpenseScreen);
    });

    updateCancel.addEventListener("click", () => {
        closeScreen(updateBudgetScreen);
    });

    confirmBudgetUpdate.addEventListener("click", async () => {
        const amount = budgetAmountInput.value;
        if (!amount || Number(amount) <= 0) {
            alert("Please enter a valid budget amount.");
            return;
        }
        const endpoint = budgetMode === "create"
            ? "/budget/create"
            : "/budget/update";
        try {

            await sendBudgetRequest(endpoint, {
                amount: amount
            });

            window.location.reload();

        } catch (error) {
            alert(error.message);
        }
    });

    addExpenseConfirm.addEventListener("click", async () => {

        const title = expenseTitleInput.value.trim();
        const amount = expenseAmountInput.value;
        const details = expenseDetailsInput.value.trim();

        if (!title || !amount || Number(amount) <= 0) {
            alert("Please complete the expense title and amount.");
            return;
        }
        try {
            await sendBudgetRequest("/budget/expense/add", {
                title: title,
                amount: amount,
                details: details
            });

            window.location.reload();

        } catch (error) {
            alert(error.message);
        }
    });

    saveChangesBtn.addEventListener("click", async () => {

        if (!selectedExpenseId) {
            alert("No expense selected.");
            return;
        }
        const title = editExpenseTitle.value.trim();
        const amount = editExpenseAmount.value;
        const details = editExpenseDetails.value.trim();
        if (!title || !amount || Number(amount) <= 0) {
            alert("Please enter a valid expense title and amount.");
            return;
        }

        try {
            await sendBudgetRequest("/budget/expense/update", {
                expense_id: selectedExpenseId,
                title: title,
                amount: amount,
                details: details
            });
            window.location.reload();

        } catch (error) {
            alert(error.message);
        }
    });

    deleteExpenseBtn.addEventListener("click", () => {

        deleteBlurOverlay.style.display = "flex";

        setTimeout(() => {
            deleteConfirm.classList.add("show");
        }, 100);

    });

    notYetBtn.addEventListener("click", () => {

        deleteConfirm.classList.remove("show");

        setTimeout(() => {
            deleteBlurOverlay.style.display = "none";
        }, 250);

    });

    yesSirBtn.addEventListener("click", async () => {

        if (!selectedExpenseId) {
            alert("No expense selected.");
            return;
        }
        try {
            await sendBudgetRequest("/budget/expense/delete", {
                expense_id: selectedExpenseId
            });

            window.location.reload();

        } catch (error) {
            alert(error.message);
        }

    });

});

async function sendBudgetRequest(url, data) {
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
        formData.append(key, value);
    });

    const csrfToken = document.querySelector(
        'meta[name="csrf-token"]'
    ).content;

    const response = await fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        },
        body: formData
    });
    const result = await response.json();
    if (!response.ok || !result.success) {
        throw new Error(result.message || "Something went wrong.");
    }

    return result;
}
