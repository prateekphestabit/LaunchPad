const addButton = document.getElementById('addBtn');
const taskInput = document.querySelector('input');
const taskList = document.getElementById('list');

let tasks = JSON.parse(localStorage.getItem("tasks")) || {};   

// Load tasks on startup
Object.keys(tasks).forEach(taskText => {
    createTaskElement(taskText, tasks[taskText]);
});


function createTaskElement(text, completed) {
    const task = document.createElement('div');
    task.id = 'task';

    const container = document.createElement('div');

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.checked = completed;

    const span = document.createElement('span');
    span.textContent = text;
    if (completed) span.style.textDecoration = "line-through";

    const del = document.createElement('span');
    del.textContent = "x";
    del.id = "delete";


    // checkbox event
    checkbox.addEventListener('change', () => {
        tasks[text] = checkbox.checked;
        span.style.textDecoration = checkbox.checked ? "line-through" : "none";
        localStorage.setItem("tasks", JSON.stringify(tasks));
    });

    // delete event
    del.addEventListener('click', () => {
        delete tasks[text];
        localStorage.setItem("tasks", JSON.stringify(tasks));
        taskList.removeChild(task);
    });

    // append elements
    task.appendChild(container);
    container.appendChild(checkbox);
    container.appendChild(span);
    task.appendChild(del);
    taskList.appendChild(task);
}

function addTask() {
    let text = taskInput.value.trim();
    if (!text) return alert("Enter task");

    if (tasks[text] !== undefined) {
        alert("Task already exists");
        return;
    }

    tasks[text] = false;
    localStorage.setItem("tasks", JSON.stringify(tasks));
    createTaskElement(text, false);
    taskInput.value = "";
}

addButton.addEventListener('click', addTask);

taskInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") addTask();
});
