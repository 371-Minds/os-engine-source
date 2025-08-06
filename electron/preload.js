const { contextBridge, ipcRenderer } = require('electron');
const { ConvexReactClient } = require('convex/react');

const convex = new ConvexReactClient("https://affable-dachshund-170.convex.cloud");

contextBridge.exposeInMainWorld('electronAPI', {
  processCode: (code) => ipcRenderer.invoke('ai:process-code', code),
  processTerminalCommand: (command) => ipcRenderer.invoke('ai:terminal-command', command),
  convex: convex,
});
