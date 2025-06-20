ZENO Electron App
ZENO is your personal AI lab assistant,fully voice-controlled, multi-modal, and equipped with futuristic features ranging from GitHub integration to gesture control and idea generation.

Getting Started
📥 1. Download the App Clone or download the ELECTRON APP folder from the branch: branch = "features/MarwaMunir"

⚙️ 2. Install Electron

Install Electron locally:

🔗 Electron Quick Start Guide: (https://www.electronjs.org/docs/latest/tutorial/quick-start)

This includes:

Installing Electron globally or locally

Setting up main.js

Running the app using npx electron . or npm start

🧪 3. Set Up Python Environment We recommend using conda, but a venv will work too.

Create and activate your environment

Install dependencies: pip install -r requirements.txt

▶️ 4. Start the App In your terminal, run:

npm start or npx electron ZENO will open and appear asleep. Wait a few seconds for the backend to fully load. A button will pop up that says:

"SPEAK: WAKE UP ZENO"

Say "Wake up Zeno" and ZENO will awaken and enter its lab.

🎙️ Voice Commands Once ZENO is awake, you can speak the following commands:

"ACTIVATE GITHUB MODE"

"ACTIVATE TERMINAL GOOGLE MODE"

"ACTIVATE WILD IDEA MODE"

"ACTIVATE GESTURE CONTROL MODE"

🔐 GitHub Mode
ZENO needs a GitHub Token to work with your GitHub account.

📌 How to Set It Up: Go to https://github.com/settings/tokens

Click Generate new token (classic)

Select scopes:

✅ repo

✅ delete_repo

Copy the token (you won’t be able to see it again)

Set it as an environment variable:

Windows:

GITHUB_TOKEN(make sure it is in capital letters) ="your_token_here"

macOS/Linux: Add this line to ~/.bashrc or ~/.zshrc: export GITHUB_TOKEN="your_token_here" Then run source ~/.bashrc or source ~/.zshrc.

🧠 GitHub Features ZENO can perform the following with voice commands:

"UPLOAD PROJECT" → ZENO will ask for:

Repository name

Description (for README)

Folder path Then upload your selected folder to GitHub.

"DISPLAY MY REPOS" → Lists all your repositories.

"ACCESS CONTENTS" → Enter repo name and ZENO will read contents.

"DELETE A REPO" → Enter repo name to delete it.

"MERGE MODE" (in development) → Provide base branch + source branch, and ZENO will merge with a commit message.

"COMMIT MODE" (in development) → Provide:

Repo name

Local folder path

Commit message

Branch name (new or existing), if you don't have a branch then just enter the name for your branch and it will automatically create it.

🌐 Google Terminal Mode
Command: "ACTIVATE TERMINAL GOOGLE MODE"

First , add a serapi key from the website to the environmental varibales with the exact name "SERPAPI_KEY" .

Speak your query — ZENO will search it silently and give back filtered results without opening a browser.

#🧪 Quantum Creativity Engine (Wild Idea Mode) Command: "ACTIVATE WILD IDEA MODE"

ZENO will ask:

Your desired domain, ( You have to pick from the domains available on screen.)

Any additional info

Then it will generate a wild creative idea using its AI engine.

#✋ Gesture Control Mode Command: "ACTIVATE GESTURE CONTROL MODE"

ZENO will:

Open your webcam

Start gesture tracking using Mediapipe

🧤 Supported Gestures Action Gesture Scroll Down Swipe vertically Scroll Up Swipe horizontally Tap (Click) Pinch thumb + index finger

🧪 Developer Tips
To test any feature individually, use the top 4 module files inside the ELECTRON APP folder , each corresponds to a separate feature.It will save the hustle of having to download the electron app locally and other depedencies.

Also if you prefer text based response, use the feature module individually rather than calling them from Zeno app.

About
No description, website, or topics provided.
Resources
 Readme
 Activity
Stars
 0 stars
Watchers
 0 watching
Forks
 0 forks
Releases
No releases published
Create a new release
Packages
No packages published
Publish your first package
Languages
Python
100.0%
Suggested workflows
Based on your tech stack
Django logo
Django
Build and Test a Django Project
Publish Python Package logo
Publish Python Package
Publish a Python Package to PyPI on release.
Pylint logo
Pylint
Lint a Python application with pylint.
More workflows
Footer
