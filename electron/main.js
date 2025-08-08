const { app, BrowserWindow, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const { autoUpdater } = require('electron-updater');

let pyProc = null;

function findPython() {
  if (process.env.PYTHON_PATH) return process.env.PYTHON_PATH;
  const bundled = process.platform === 'win32'
    ? path.join(process.resourcesPath, 'python', 'python.exe')
    : path.join(process.resourcesPath, 'python', 'bin', 'python3');
  if (fs.existsSync(bundled)) return bundled;
  return process.platform === 'win32' ? 'python.exe' : 'python3';
}

async function waitFor(url, timeoutMs = 30000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try { const r = await fetch(url, { timeout: 2000 }); if (r.ok) return true; } catch {}
    await new Promise(r => setTimeout(r, 500));
  }
  return false;
}

function spawnPython(pyPath) {
  const script = path.join(__dirname, '..', 'launch_5470_pro.py');
  pyProc = spawn(pyPath, [script], { cwd: path.join(__dirname, '..') });
  pyProc.stdout.on('data', d => console.log('[py]', d.toString().trim()));
  pyProc.stderr.on('data', d => console.error('[py-err]', d.toString().trim()));
  pyProc.on('exit', c => console.log('[py] exited', c));
}

async function createWindow() {
  const win = new BrowserWindow({ width: 1100, height: 800, webPreferences: { contextIsolation: true }});
  await win.loadURL('http://localhost:8001');
}

function setupAutoUpdater() {
  app.setAppUserModelId('es.blockchain5470.wallet');
  autoUpdater.autoDownload = true;
  autoUpdater.on('update-downloaded', async () => {
    const res = await dialog.showMessageBox({
      type: 'info', buttons: ['Reiniciar ahora', 'Después'], defaultId: 0,
      title: 'Actualización lista', message: 'Hay una nueva versión. ¿Reiniciar para actualizar?'
    });
    if (res.response === 0) autoUpdater.quitAndInstall();
  });
}

const gotLock = app.requestSingleInstanceLock();
if (!gotLock) app.quit();

app.whenReady().then(async () => {
  setupAutoUpdater(); autoUpdater.checkForUpdatesAndNotify();
  const py = findPython();
  spawnPython(py);
  await waitFor('http://localhost:8001', 30000);
  await createWindow();
});

app.on('before-quit', () => { try { if (pyProc && !pyProc.killed) pyProc.kill(); } catch {} });
