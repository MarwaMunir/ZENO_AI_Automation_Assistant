// main.js
const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');



let mainWindow;

function createWindow () {
  mainWindow = new BrowserWindow({
    width: 600,
    height: 720,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      enableRemoteModule: false
      
    },
  });

  mainWindow.loadFile('index.html');

  // Launch Python script
  const python = spawn('python', ['zeno_voiceAssistant.py']);
   python.stdout.on('data', (data) => {
    console.log("Received data from Python:", data.toString());


    try {
      const messages = data.toString().trim().split("\n");
      messages.forEach((message) => {
        const parsed = JSON.parse(message);
        if (parsed.event === "mic_started") {
           mainWindow.webContents.send('show-wake-popup'); // Show button early
        }  
        if (parsed.event === "wake_word_detected") {
          mainWindow.webContents.send('zeno-awake');
        }
        if (parsed.event === "command_detected") {
          mainWindow.webContents.send('zeno-work');
        }
        if (parsed.event === "goodbye_detected") {
          mainWindow.webContents.send('zeno-goodbye');
        }
        if (parsed.event === "google_search_result") {
          mainWindow.webContents.send('google-search-result', parsed.data);
        }
        if (parsed.event === "moods_triggered") {
          mainWindow.webContents.send('moods-triggered', parsed.data);
        }
        if (parsed.event === "domains_triggered") {
          mainWindow.webContents.send('domains-triggered', parsed.data);
        }
        if (parsed.event === "wild_idea_result") {
          mainWindow.webContents.send('wild-idea-result', parsed.data);
        }
        if (parsed.event === "display_all_repos") {
          mainWindow.webContents.send('display-all-repos', parsed.data);
        }
        if (parsed.event === "access_contents_of_repo") {
          mainWindow.webContents.send('access-contents-of-repo', parsed.data);
        }
        if (parsed.event === "folder_path") {
          mainWindow.webContents.send('folder-path', parsed.data);
        }



        
      });
    } catch (err) {
      console.error("Failed to parse message from Python:", data.toString());
    }
  });

  ipcMain.handle('open-folder-dialog', async () => {
    const result = await dialog.showOpenDialog({
      properties: ['openDirectory']
    });
    if (result.canceled) return null;
    const folderPath = result.filePaths[0];

    // ✅ SEND TO PYTHON BACKEND
    const message = {
      event: "user_selected_folder_path",
      data: {
        folder_path: folderPath
      }
    };

    python.stdin.write(JSON.stringify(message) + "\n");
    return folderPath;
  });

  


 
}

app.whenReady().then(createWindow);

