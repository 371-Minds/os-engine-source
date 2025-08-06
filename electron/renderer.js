import { ConvexReactClient } from "convex/react";
import { api } from "../convex/_generated/api";
import { cacheQAPairs, getCachedQAPairs } from "./idb.js";

const convex = new ConvexReactClient(process.env.CONVEX_URL);

const qaList = document.getElementById("qaList");
const askQuestionForm = document.getElementById("askQuestionForm");
const questionInput = document.getElementById("questionInput");
const statusDiv = document.getElementById("status");
const agentTaskForm = document.getElementById("agentTaskForm");
const agentTaskInput = document.getElementById("agentTaskInput");

function render(qa_pairs) {
    qaList.innerHTML = "";
    qa_pairs.forEach(pair => {
        const li = document.createElement("li");
        li.innerHTML = `<strong>Q:</strong> ${pair.question}<br><strong>A:</strong> ${pair.answer}`;
        if (pair.result) {
            li.innerHTML += `<br><strong>Result:</strong> ${pair.result}`;
        }
        qaList.appendChild(li);
    });
}

async function loadInitialView() {
    statusDiv.textContent = "Loading cached history...";
    try {
        const cachedPairs = await getCachedQAPairs();
        if (cachedPairs.length > 0) {
            render(cachedPairs);
            statusDiv.textContent = "Offline (displaying cached history)";
        } else {
            statusDiv.textContent = "No cached history found. Please connect to ask a question.";
        }
    } catch (error) {
        console.error("Failed to load cached history:", error);
        statusDiv.textContent = "Error loading cache. Please connect.";
    }
}

// Load cached history on startup
loadInitialView();

// This will run when Convex connection is established
convex.onUpdate(api.qa.getHistory, {}, async (qa_pairs) => {
    render(qa_pairs);
    await cacheQAPairs(qa_pairs);
});

askQuestionForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const question = questionInput.value;
    if (question) {
        try {
            await convex.mutation(api.qa.ask, { question: question });
            questionInput.value = "";
        } catch (error) {
            console.error("Failed to ask question:", error);
            alert("Failed to ask question. You might be offline.");
        }
    }
});

agentTaskForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const task = agentTaskInput.value;
    if (task) {
        try {
            await convex.mutation(api.agentTasks.addAgentTask, { task: task });
            agentTaskInput.value = "";
        } catch (error) {
            console.error("Failed to add agent task:", error);
            alert("Failed to add agent task. You might be offline.");
        }
    }
});

convex.connectionState.onUpdate((state) => {
    // We get a more detailed status from the onUpdate handler for qa_pairs
    if (state.type === 'connected') {
        statusDiv.textContent = "Status: Connected";
    } else {
        statusDiv.textContent = `Status: ${state.type}`;
    }
});
