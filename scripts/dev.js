const { spawn } = require('child_process');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');

console.log('\x1b[36m%s\x1b[0m', '>>> Starting Antigravity Study Platform (FastAPI Backend + Vite Frontend)...');

// 1. Start FastAPI server
const apiProc = spawn(process.platform === 'win32' ? 'python' : 'python3', ['-m', 'uvicorn', 'api.index:app', '--reload', '--port', '8000'], {
  cwd: rootDir,
  stdio: 'inherit',
  shell: true
});

// 2. Start Vite dev server
const npmCmd = process.platform === 'win32' ? 'npm.cmd' : 'npm';
const webProc = spawn(npmCmd, ['run', 'dev'], {
  cwd: path.join(rootDir, 'web'),
  stdio: 'inherit',
  shell: true
});

const cleanup = () => {
  console.log('\n\x1b[33m%s\x1b[0m', 'Shutting down dev servers...');
  try { apiProc.kill(); } catch {}
  try { webProc.kill(); } catch {}
  process.exit(0);
};

process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);
