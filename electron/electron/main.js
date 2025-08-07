const { app, BrowserWindow, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const { autoUpdater } = require('electron-updater');

let pyChain = null;
let pyWallet = null;

function findPython() {
  if (process.env.PYTHON_PATH) return process.env.PYTHON_PATH;
  const bundled = process.platform === 'win32'
    ? path.join(process.resourcesPath, 'python', 'python.exe')
    : path.join(process.resourcesPath, 'python', 'bin', 'python3');
  if (fs.existsSync(bundled)) return bundled;
  return process.platform === 'win32' ? 'python.exe' : 'python3';
}

async function waitFor(url, timeoutMs = 20000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const r = await fetch(url, { timeout: 2000 });
      if (r.ok) return true;
    } catch (_) {}
    await new Promise(r => setTimeout(r, 500));
  }
  return false;
}

function spawnChain(pyPath) {
  const script = path.join(__dirname, '..', 'blockchain_5470_synced_ai_zk.py');
  pyChain = spawn(pyPath, [script], { cwd: path.join(__dirname, '..') });
  pyChain.stdout.on('data', d => console.log('[chain]', d.toString().trim()));
  pyChain.stderr.on('data', d => console.error('[chain-err]', d.toString().trim()));
  pyChain.on('exit', (c) => console.log('[chain] exited', c));
}

function spawnWallet(pyPath) {
  const script = path.join(__dirname, '..', 'wallet.py'); // tu wallet
  pyWallet = spawn(pyPath, [script], { cwd: path.join(__dirname, '..') });
  pyWallet.stdout.on('data', d => console.log('[wallet]', d.toString().trim()));
  pyWallet.stderr.on('data', d => console.error('[wallet-err]', d.toString().trim()));
  pyWallet.on('exit', (c) => console.log('[wallet] exited', c));
}

async function createWindow() {
  const win = new BrowserWindow({
    width: 1100,
    height: 800,
    webPreferences: { nodeIntegration: false, contextIsolation: true }
  });
  await win.loadURL('http://localhost:8001');
}

function setupAutoUpdater() {
  app.setAppUserModelId('es.blockchain5470.wallet');
  autoUpdater.autoDownload = true;
  autoUpdater.on('update-downloaded', async () => {
    const res = await dialog.showMessageBox({
      type: 'info',
      buttons: ['Reiniciar ahora', 'Después'],
      defaultId: 0,
      title: 'Actualización lista',
      message: 'Hay una nueva versión descargada. ¿Reiniciar para actualizar?'
    });
    if (res.response === 0) autoUpdater.quitAndInstall();
  });
}

const gotLock = app.requestSingleInstanceLock();
if (!gotLock) app.quit();

app.whenReady().then(async () => {
  setupAutoUpdater();
  autoUpdater.checkForUpdatesAndNotify();

  const py = findPython();
  spawnChain(py);
  const okChain = await waitFor('http://localhost:5000/health', 30000);
  if (!okChain) console.warn('chain health timeout');

  spawnWallet(py);
  const okWallet = await waitFor('http://localhost:8001', 30000);
  if (!okWallet) console.warn('wallet server timeout');

  await createWindow();
});

app.on('before-quit', () => {
  try { if (pyWallet && !pyWallet.killed) pyWallet.kill(); } catch {}
  try { if (pyChain && !pyChain.killed) pyChain.kill(); } catch {}
});
