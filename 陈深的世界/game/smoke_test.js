// 冒烟测试：加载主界面并验证渲染器正常，然后退出
const { app, BrowserWindow } = require('electron');
const path = require('path');

app.whenReady().then(() => {
  const win = new BrowserWindow({ show: false, webPreferences: { nodeIntegration: false, contextIsolation: true } });
  let done = false;
  win.webContents.on('did-finish-load', async () => {
    if (done) return; done = true;
    try {
      const info = await win.webContents.executeJavaScript(`({
        title: document.title,
        hub: !!document.getElementById('hub'),
        modes: !!document.getElementById('modeWorld') && !!document.getElementById('modeStory'),
        photosInGallery: (document.getElementById('galGrid') ? 'yes' : 'no')
      })`);
      console.log('SMOKE_OK ' + JSON.stringify(info));
    } catch (e) {
      console.log('SMOKE_JS_ERR ' + e.message);
    }
    setTimeout(() => app.exit(0), 300);
  });
  win.webContents.on('did-fail-load', (e, code, desc) => {
    console.log('SMOKE_LOAD_FAIL ' + code + ' ' + desc);
    app.exit(1);
  });
  win.loadFile(path.join(__dirname, 'index.html'));
});
