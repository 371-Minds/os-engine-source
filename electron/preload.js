const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  processCode: (code) => ipcRenderer.invoke('ai:process-code', code),
  processTerminalCommand: (command) => ipcRenderer.invoke('ai:terminal-command', command)
});
