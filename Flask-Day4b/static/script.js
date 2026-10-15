
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("taskForm");
    const titleInput = document.getElementById("title");
    const taskList = document.getElementById("taskList");
    const feedback = document.getElementById("feedback");
    const emptyMessage = document.getElementById("emptyMessage");
    const addButton = document.getElementById("addButton");

    form.addEventListener("submit", async function (event) {
        // Prevent the normal form submission and page reload
        event.preventDefault();

        const title = titleInput.value.trim();

        if (!title) {
            feedback.textContent = "Please enter a task title.";
            feedback.classList.add("error-text");
            return;
        }

        addButton.disabled = true;
        feedback.textContent = "Adding task...";
        feedback.classList.remove("error-text");

        try {
            // Send the new task to Flask
            const response = await fetch("/add_task", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ title: title })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.message || "Could not add task.");
            }

            // Create a new table row without reloading
            const row = document.createElement("tr");

            const idCell = document.createElement("td");
            idCell.textContent = data.task.id;

            const titleCell = document.createElement("td");
            titleCell.textContent = data.task.title;

            const statusCell = document.createElement("td");
            const statusLabel = document.createElement("span");
            statusLabel.className = "status";
            statusLabel.textContent = data.task.status;
            statusCell.appendChild(statusLabel);

            row.append(idCell, titleCell, statusCell);

            // Display the newest task at the top
            taskList.prepend(row);

            emptyMessage.hidden = true;
            titleInput.value = "";
            feedback.textContent = "Task added successfully!";
        } catch (error) {
            feedback.textContent = error.message;
            feedback.classList.add("error-text");
        } finally {
            addButton.disabled = false;
        }
    });
});
