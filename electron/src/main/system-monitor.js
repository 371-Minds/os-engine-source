const chokidar = require('chokidar');
const { clipboard } = require('electron');
const fs = require('fs');

class SystemMonitor {
  constructor(aiOrchestrator) {
    this.aiOrchestrator = aiOrchestrator;
    this.watchers = new Map();
    this.clipboardHistory = [];
    this.startClipboardMonitoring();
  }

  startWatching(projectPath) {
    const watcher = chokidar.watch(projectPath, {
      ignored: /(^|[\/\\])\../,
      persistent: true
    });

    watcher.on('change', (path) => this.handleFileChange(path));
    watcher.on('add', (path) => this.handleFileAdd(path));
    
    this.watchers.set(projectPath, watcher);
    return { success: true, watching: projectPath };
  }

  handleFileChange(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    // Send to AI for analysis
    this.aiOrchestrator.processFileChange(filePath, content);
  }

  startClipboardMonitoring() {
    let lastClipboardContent = clipboard.readText();
    
    setInterval(() => {
      const newContent = clipboard.readText();
      if (newContent !== lastClipboardContent && newContent.length > 0) {
        lastClipboardContent = newContent;
        this.clipboardHistory.push({
          content: newContent,
          timestamp: Date.now()
        });
        // Process clipboard content with AI
        this.processClipboardContent(newContent);
      }
    }, 1000);
  }

  processClipboardContent(content) {
    // Check if it's code, send to appropriate AI agent
    if (this.isCode(content)) {
      this.aiOrchestrator.processCode(content);
    }
  }

  isCode(text) {
    // Simple heuristic to detect code
    return /[{}();]/.test(text) || text.includes('function') || text.includes('const ');
  }
}

module.exports = SystemMonitor;
