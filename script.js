// Global array to store tasks
let tasks = [];

// Function to render all tasks in the table
function renderTasks() {
  const tableBody = document.getElementById("task-table-body");
  tableBody.innerHTML = ""; // Clear the table before re-rendering

  tasks.forEach((task, index) => {
    const row = document.createElement("tr");

    // Column 1: Task number
    const numberCell = document.createElement("td");
    numberCell.textContent = index + 1;

    // Column 2: Task text
    const taskCell = document.createElement("td");
    taskCell.textContent = task.text;
    taskCell.className = task.done ? "done" : ""; // Apply 'done' class if task is completed

    // Column 3: Checkbox
    const checkCell = document.createElement("td");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = task.done;
    
    // Event listener to mark a task as done/undone
    checkbox.addEventListener("change", () => {
      tasks[index].done = checkbox.checked;
      renderTasks(); // Re-render the list to show the change (the line-through)
    });

    checkCell.appendChild(checkbox);

    // Add all cells to the row
    row.appendChild(numberCell);
    row.appendChild(taskCell);
    row.appendChild(checkCell);

    // Add the row to the table body
    tableBody.appendChild(row);
  });
}

// --- Event Listeners for Buttons ---

// Add Task
document.getElementById("add-btn").addEventListener("click", function () {
  const taskInput = document.getElementById("task-input");
  const taskName = taskInput.value.trim();

  if (taskName !== "") {
    tasks.push({ text: taskName, done: false });
    taskInput.value = ""; // Clear the input box
    renderTasks(); // Update the table
  }
});

// Update Task (Improved to use Task Number)
document.getElementById("update-btn").addEventListener("click", function () {
  const taskNumberInput = document.getElementById("old-task");
  const newTaskTextInput = document.getElementById("new-task");
  
  // Get the number and convert it to a zero-based index
  const taskIndex = parseInt(taskNumberInput.value, 10) - 1;
  const newTaskText = newTaskTextInput.value.trim();

  // Check if the index is valid and there's new text
  if (!isNaN(taskIndex) && tasks[taskIndex] && newTaskText !== "") {
    tasks[taskIndex].text = newTaskText;
    taskNumberInput.value = "";
    newTaskTextInput.value = "";
    renderTasks();
  } else {
    alert("Please enter a valid task number and new task text.");
  }
});

// Delete Task (Improved to use Task Number)
document.getElementById("delete-btn").addEventListener("click", function () {
  const taskNumberInput = document.getElementById("delete-task");

  // Get the number and convert it to a zero-based index
  const taskIndex = parseInt(taskNumberInput.value, 10) - 1;

  // Check if the index is valid (exists in the tasks array)
  if (!isNaN(taskIndex) && tasks[taskIndex]) {
    tasks.splice(taskIndex, 1); // Remove 1 item at the given index
    taskNumberInput.value = "";
    renderTasks();
  } else {
    alert("Please enter a valid task number to delete.");
  }
});

// View Tasks (This button now implicitly works because adding/deleting already updates the view)
// We can still keep it to manually refresh the table if needed.
document.getElementById("view-btn").addEventListener("click", function () {
  renderTasks();
});

// Initial render in case there are saved tasks in the future
renderTasks();