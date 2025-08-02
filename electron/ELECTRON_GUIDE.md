# Implementation Guide: Integrating 371 Minds OS with Electron.js

This guide provides step-by-step instructions for packaging the 371 Minds OS Python backend and integrating it with an Electron.js desktop application.

**Goal:** To run the Python-based agent system as a background process and communicate with it from an Electron frontend, allowing you to build a native desktop UI for the 371 Minds OS.

**Core Strategy:**
1.  **Backend:** Wrap the Python agent system in a Flask web server that listens for local API requests.
2.  **Packaging:** Package the entire Python application (including all dependencies and the Flask server) into a single standalone executable using PyInstaller.
3.  **Frontend:** Create an Electron.js application that, on startup, launches the packaged Python executable as a child process.
4.  **Communication:** The Electron app's JavaScript code will make `fetch` requests to the local Flask server (`http://127.0.0.1:5000`) to send tasks and receive results.

This approach allows you to keep the powerful Python backend while providing a rich user experience with a modern web-based frontend in Electron.

---

## Part 1: Preparing the Python Backend

In this part, we will prepare the Python application to run as a web server and then package it into a distributable executable.

### Step 1.1: The Web Server (`server.py`)

We have already created a `server.py` file that wraps the agent system in a Flask application. This server exposes an `/api/execute` endpoint to process tasks. Here is the code for reference:

```python
# server.py
import os
import sys
import asyncio
from pathlib import Path
from flask import Flask, request, jsonify

# Add current directory to path for local imports
sys.path.append(str(Path(__file__).parent))

from router_agent import IntelligentRoutingSystem
from repo_intake_agent import RepoIntakeAgent
from analytics_371 import Analytics371
from base_agent import Task, AgentType

# --- System Initialization ---
print("Initializing 371 Minds OS components...")
api_key = os.getenv('POSTHOG_API_KEY', 'demo_key_12345')
analytics = Analytics371(api_key)
router = IntelligentRoutingSystem()
repo_intake_agent = RepoIntakeAgent(analytics_client=analytics)
router.register_agent(repo_intake_agent)
print("System components initialized successfully.")

# --- Flask Web Server ---
app = Flask(__name__)

@app.route('/api/execute', methods=['POST'])
def execute_task():
    data = request.get_json()
    submission_text = data.get('submission')
    if not submission_text:
        return jsonify({"error": "Invalid payload: 'submission' field is required"}), 400

    print(f"Received task via API: '{submission_text}'")
    initial_task = Task(
        id="api_task_001",
        description="Top-level API request",
        agent_type=AgentType.INTELLIGENT_ROUTER,
        payload={"submission": submission_text, "user_id": "electron_user"}
    )
    final_task_state = asyncio.run(router.execute_task(initial_task))
    
    if final_task_state.status.value == "completed":
        return jsonify({"status": "success", "result": final_task_state.result}), 200
    else:
        return jsonify({"status": "error", "error": final_task_state.result.get('error')}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
```

### Step 1.2: Update Dependencies

We've already added `Flask` to the `requirements.txt` file. Ensure your `requirements.txt` is up-to-date, then install all dependencies into a virtual environment.

```bash
# It's highly recommended to use a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install all dependencies
pip install -r requirements.txt
```

### Step 1.3: Package the Application with PyInstaller

Now, we'll package the entire Python application into a single executable. This executable will contain the Python interpreter, all the code, and all the dependencies.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Run PyInstaller:**
    The following command tells PyInstaller to build a single-file executable (`--onefile`) from our `server.py` script. We also need to tell it where to find the other Python files (`--paths=.`).
    ```bash
    pyinstaller --onefile --paths=. --name="minds-os-backend" server.py
    ```

3.  **Locate the Executable:**
    After the process completes, you will find the executable in the `dist` directory.
    -   On macOS/Linux: `dist/minds-os-backend`
    -   On Windows: `dist/minds-os-backend.exe`

You can test the executable by running it directly from your terminal. You should see the Flask server start up.

```bash
./dist/minds-os-backend
```

---

## Part 2: Setting Up the Electron Frontend

Now we will create the Electron application that will serve as the user interface.

### Step 2.1: Create a New Electron Project

If you don't have an existing Electron project, you can create one easily.

```bash
# Create a new directory for your Electron app
mkdir electron-ui && cd electron-ui

# Initialize a new Node.js project
npm init -y

# Install Electron
npm install --save-dev electron
```

### Step 2.2: Basic Project Structure

Create the following files in your `electron-ui` directory:

-   `main.js` (The main Electron process)
-   `index.html` (The UI for our application)
-   `renderer.js` (JavaScript for the UI)
-   `preload.js` (Script to securely expose Node.js APIs to the renderer)

Update your `package.json` to include a start script and point to `main.js`:
```json
{
  "name": "electron-ui",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": {
    "start": "electron ."
  },
  "devDependencies": {
    "electron": "^28.0.0" 
  }
}
```

### Step 2.3: Copy the Python Executable

Copy the `minds-os-backend` executable from your Python project's `dist` folder into a new `backend` directory inside your `electron-ui` project.

- `electron-ui/`
  - `backend/`
    - `minds-os-backend` (or `minds-os-backend.exe`)
  - `node_modules/`
  - `index.html`
  - `main.js`
  - `package.json`
  - ...

### Step 2.4: Spawn the Backend Process from Electron

In `main.js`, we will write the code to launch our Python backend when the Electron app starts.

```javascript
// main.js
const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let backendProcess = null;

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  });
  win.loadFile('index.html');
}

app.whenReady().then(() => {
  // Determine the path to the backend executable
  const backendPath = path.join(__dirname, 'backend', process.platform === 'win32' ? 'minds-os-backend.exe' : 'minds-os-backend');
  
  // Spawn the backend process
  backendProcess = spawn(backendPath);

  backendProcess.stdout.on('data', (data) => {
    console.log(`Backend stdout: ${data}`); // For debugging
  });
  backendProcess.stderr.on('data', (data) => {
    console.error(`Backend stderr: ${data}`); // For debugging
  });

  createWindow();
});

// Quit the backend process when the app closes
app.on('will-quit', () => {
  if (backendProcess) {
    backendProcess.kill();
  }
});
```

---

## Part 3: Bridging the Gap (UI and Communication)

Finally, let's create the UI and write the JavaScript to communicate with the local Python server.

### Step 3.1: Create the User Interface (`index.html`)

This is a simple HTML file with a textarea for input and a button to submit the task.

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>371 Minds OS</title>
</head>
<body>
    <h1>371 Minds OS Interface</h1>
    <textarea id="taskInput" rows="4" cols="50" placeholder="Enter your task..."></textarea>
    <br>
    <button id="submitBtn">Execute Task</button>
    <hr>
    <h2>Result:</h2>
    <pre id="resultOutput"></pre>

    <script src="renderer.js"></script>
</body>
</html>
```

### Step 3.2: Write the Renderer Logic (`renderer.js`)

This script handles the button click, sends the request to the Python backend, and displays the result.

```javascript
// renderer.js
document.getElementById('submitBtn').addEventListener('click', () => {
    const task = document.getElementById('taskInput').value;
    const output = document.getElementById('resultOutput');
    output.textContent = 'Processing...';

    // The fetch request to our local Python server
    fetch('http://127.0.0.1:5000/api/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ submission: task }),
    })
    .then(response => response.json())
    .then(data => {
        output.textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error('Error:', error);
        output.textContent = 'Error: ' + error.message;
    });
});
```

### Step 3.3: Run the Application

You are now ready to run your fully integrated application!

From inside the `electron-ui` directory, run:
```bash
npm start
```

Your Electron application should launch, and you can now enter a task (e.g., "Analyze the repository at https://github.com/371-minds/os-engine-source") and see the result from the Python backend displayed in the UI.

This guide provides a solid foundation. You can expand on this by adding more sophisticated UI elements, handling multiple concurrent tasks, or adding more API endpoints to the Python server.
