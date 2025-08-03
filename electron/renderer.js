import { ConvexReactClient } from "convex/react";
import { api } from "../convex/_generated/api";
import { cacheTasks, getCachedTasks } from "./idb.js";

const convex = new ConvexReactClient(process.env.CONVEX_URL);

const taskList = document.getElementById("taskList");
const addTaskForm = document.getElementById("addTaskForm");
const taskInput = document.getElementById("taskInput");
const statusDiv = document.getElementById("status");

function render(tasks) {
    taskList.innerHTML = "";
    tasks.forEach(task => {
        const li = document.createElement("li");
        li.textContent = task.body;
        if (task.isCompleted) {
            li.classList.add("completed");
        }
        taskList.appendChild(li);
    });
}

async function loadInitialView() {
    statusDiv.textContent = "Loading cached tasks...";
    try {
        const cachedTasks = await getCachedTasks();
        if (cachedTasks.length > 0) {
            render(cachedTasks);
            statusDiv.textContent = "Offline (displaying cached tasks)";
        } else {
            statusDiv.textContent = "No cached tasks found. Please connect to add tasks.";
        }
    } catch (error) {
        console.error("Failed to load cached tasks:", error);
        statusDiv.textContent = "Error loading cache. Please connect.";
    }
}

// Load cached tasks on startup
loadInitialView();

// This will run when Convex connection is established
convex.onUpdate(api.tasks.get, {}, async (tasks) => {
    render(tasks);
    await cacheTasks(tasks);
});

addTaskForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const taskBody = taskInput.value;
    if (taskBody) {
        try {
            await convex.mutation(api.tasks.add, { body: taskBody });
            taskInput.value = "";
        } catch (error) {
            console.error("Failed to add task:", error);
            alert("Failed to add task. You might be offline.");
        }
    }
});

convex.connectionState.onUpdate((state) => {
    // We get a more detailed status from the onUpdate handler for tasks
    if (state.type === 'connected') {
        statusDiv.textContent = "Status: Connected";
    } else {
        statusDiv.textContent = `Status: ${state.type}`;
    }
});
