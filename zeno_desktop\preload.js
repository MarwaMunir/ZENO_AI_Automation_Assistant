// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  onShowWakepopup: (callback) => ipcRenderer.on('show-wake-popup', callback),  // FIXED name
  onZenoAwake: (callback) => ipcRenderer.on('zeno-awake', callback),
  sendManualWake: () => ipcRenderer.send('manual-awake'),
  onZenoWork:(callback)=> ipcRenderer.on('zeno-work', callback), 
  onZenoGoodbye:(callback)=> ipcRenderer.on('zeno-goodbye', callback),
  onGoogleSearchResult: (callback) => ipcRenderer.on('google-search-result', (event,data) =>callback(data)),
  onMoodsTriggered: (callback)=> ipcRenderer.on('moods-triggered',(event,data)=>callback(data)),
  onDomainsTriggered: (callback)=> ipcRenderer.on('domains-triggered',(event,data)=>callback(data)),
  onWildIdeaResult: (callback)=> ipcRenderer.on('wild-idea-result',(event,data)=>callback(data)),
  onDisplayAllRepos: (callback)=> ipcRenderer.on('display-all-repos',(event,data)=>callback(data)),
  onAccessContentsOfRepo: (callback)=> ipcRenderer.on('access-contents-of-repo',(event,data)=>callback(data)),
  onFolderPath: (callback) => ipcRenderer.on('folder-path', (event, data) => callback(data)),
  selectFolderPath: ()=> ipcRenderer.invoke('open-folder-dialog'),
  sendFolderPathToBackend: (path) =>ipcRenderer.send('send-folder-path,path'),
    
    
});

