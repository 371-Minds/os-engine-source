const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const AIOrchestrator = require('./src/main/ai-orchestrator');
const SystemMonitor = require('./src/main/system-monitor');
const KnowledgeDB = require('./src/main/knowledge-db');

class AIIDEApp {
  constructor() {
    this.aiOrchestrator = new AIOrchestrator();
    this.systemMonitor = new SystemMonitor(this.aiOrchestrator);
    this.knowledgeDB = new KnowledgeDB();
    this.mainWindow = null;
  }

  async createWindow() {
    this.mainWindow = new BrowserWindow({
      width: 1400,
      height: 900,
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true,
        preload: path.join(__dirname, 'preload.js')
      }
    });

    await this.mainWindow.loadFile('src/renderer/index.html');
    this.setupIPC();
  }

  setupIPC() {
    // AI agent communication
    ipcMain.handle('ai:process-code', async (event, code) => {
      return await this.aiOrchestrator.processCode(code);
    });

    ipcMain.handle('ai:terminal-command', async (event, command) => {
      return await this.aiOrchestrator.processTerminalCommand(command);
    });

    // System monitoring
    ipcMain.handle('system:start-monitoring', async (event, path) => {
      return this.systemMonitor.startWatching(path);
    });
  }
}

const ideApp = new AIIDEApp();

app.whenReady().then(() => ideApp.createWindow());
