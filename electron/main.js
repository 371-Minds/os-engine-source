const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let backendProcess = null;

function createWindow() {
  const win = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });
  win.loadFile(path.join(__dirname, 'src/renderer/index.html'));
}

app.whenReady().then(() => {
  // Path to the Python script
  const pythonScript = path.join(__dirname, 'server.py');

  // Path to the python executable in a virtual environment
  // This makes the assumption that a 'venv' exists in the project root.
  // A more robust solution might find python3 in the PATH.
  const pythonExecutable = process.platform === 'win32'
    ? path.join(__dirname, '../../venv/Scripts/python.exe')
    : path.join(__dirname, '../../venv/bin/python');

  console.log(`Spawning backend process: ${pythonExecutable} ${pythonScript}`);

  // Spawn the backend process
  backendProcess = spawn(pythonExecutable, [pythonScript], {
    // The CWD must be the directory containing server.py so that its internal imports work
    cwd: __dirname,
    // The following options are for debugging the backend process from the Electron main process logs
    stdio: ['pipe', 'pipe', 'pipe', 'ipc']
  });

  backendProcess.stdout.on('data', (data) => {
    console.log(`Backend stdout: ${data}`);
  });
  backendProcess.stderr.on('data', (data) => {
    console.error(`Backend stderr: ${data}`);
  });
  backendProcess.on('close', (code) => {
    console.log(`Backend process exited with code ${code}`);
  });

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// Quit the backend process when the app closes
app.on('will-quit', () => {
  if (backendProcess) {
    console.log('Killing backend process...');
    backendProcess.kill();
  }
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
