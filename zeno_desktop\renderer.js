// renderer.js
console.log("✅ Renderer loaded");

document.addEventListener("DOMContentLoaded", () => {
  const backgroundMusic = document.getElementById("background-music");
  const wakeButton = document.getElementById("wakeButton");
  const video = document.getElementById("video-bg");
  const resultContainer = document.getElementById('search-results');
  const moodsContainer = document.getElementById('moods-results');
  const domainsContainer = document.getElementById('domains-results');
  const ideaContainer = document.getElementById('wild-idea-results');
  const reposContainer = document.getElementById('repos-results');
  const contentsContainer = document.getElementById('repo-contents-results');


  // music touch
  backgroundMusic.volume = 0.06;
  backgroundMusic.play().catch(() => {
    console.log("Autoplay blocked, waiting for user interaction");
  });

  document.body.addEventListener("click", () => {
    backgroundMusic.play();
  });

  let awakeTriggered = false;
  let workTriggered = false;
  let goodbyeTriggered = false;

  // Electron events
  window.electronAPI.onShowWakepopup(() => {
    console.log("Received show-wake-button event");
    wakeButton.style.display = "block";
  });

  window.electronAPI.onZenoAwake(() => {
    if (!awakeTriggered) {
      awakeTriggered = true;
      console.log("Received zeno-awake event");
      video.pause();
      video.src = "zeno_awake_finall.mp4";
      video.load();
      video.play();
      wakeButton.style.display = "none";
    }
  });

  window.electronAPI.onZenoWork(() => {
    if (!workTriggered) {
      workTriggered = true;
      console.log("Received zeno-work event");
      video.pause();
      video.src = "zeno_work.mp4";
      video.load();
      video.play();
      wakeButton.style.display = "none";
    }
  });

  window.electronAPI.onZenoGoodbye(() => {
    if (!goodbyeTriggered) {
      goodbyeTriggered = true;
      console.log("Received zeno-goodbye event");
      video.pause();
      video.src = "zeno_goodbye.mp4";
      video.load();
      video.play();
      wakeButton.style.display = "none";
    }
  });
  
  

  function showSearchResult(data) {
    if (!resultContainer) {
      console.error("Missing #search-results element in DOM");
      return;
    }

    // Create result box
    const resultBox = document.createElement('div');
    resultBox.className = 'google-result-box';
    resultBox.innerHTML = `
      <p><strong>Result ${data.number}:</strong> <a href="${data.url}" target="_blank">${data.url}</a></p>
    `;
    resultContainer.appendChild(resultBox);

    // Show the container
    resultContainer.style.display = "block";

    // Auto-hide after 15 seconds
    setTimeout(() => {
      resultContainer.style.display = "none";
    }, 15000);
  }

  window.electronAPI.onGoogleSearchResult((data) => {
    console.log("Got search result:", data);
    showSearchResult(data);
  });

  function showMoodsResult(data) {
    console.log("Inside showMoodsResult", data);
    if (!moodsContainer) return;
    const box = document.createElement('div');
    box.className = 'neon-box';
    box.innerHTML = `
      <p><strong>Choose your mood:</strong></p>
      <ul>${data.moods.map(mood => `<li>${mood}</li>`).join('')}</ul>
    `;

    
    moodsContainer.appendChild(box);
    moodsContainer.style.display = "block";



    setTimeout(() => {
      moodsContainer.style.display = "none";
    }, 9000);
  }

  window.electronAPI.onMoodsTriggered((data) => {
    console.log("Received moods:", data);
    showMoodsResult(data);
  });

  function showDomainsResult(data) {
    if (!domainsContainer) return;

    const box = document.createElement('div');
    box.className = 'neon-box';
    box.innerHTML = `
      <p><strong>Choose a domain:</strong></p>
      <ul>${data.domains.map(domain => `<li>${domain}</li>`).join('')}</ul>
    `;
    
    domainsContainer.appendChild(box);
    domainsContainer.style.display = "block";

    setTimeout(() => {
      domainsContainer.style.display = "none";
    }, 9000);
  }

  window.electronAPI.onDomainsTriggered((data) => {
    console.log("Received domains:", data);
    showDomainsResult(data);
  });

  function showWildIdeaResult(data) {
    console.log("Inside showWildIdeaResult", data);
    if (!ideaContainer) return;

    const box = document.createElement('div');
    box.className = 'neon-box';
    box.innerHTML = `
      <p><strong>Quantum Seed:</strong> ${data.seed}</p>
      <p><strong>Idea:</strong> ${data.idea}</p>
    `;
    ideaContainer.appendChild(box);
    ideaContainer.style.display = "block";

    setTimeout(() => {
      ideaContainer.style.display = "none";
    }, 120000);
  }

  window.electronAPI.onWildIdeaResult((data) => {
    console.log("Received wild idea result:", data);
    showWildIdeaResult(data);
  });

  function showReposResult(data) {
    if (!reposContainer) return;

    const box = document.createElement('div');
    box.className = 'neon-box';
    box.innerHTML = `
      <p><strong>Your GitHub Repositories:</strong></p>
      <ul>
        ${data.repositories.map(repo => `
          <li>
            <strong>${repo.name}</strong><br>
            ${repo.description || "No description"}<br>
            <a href="${repo.url}" target="_blank">${repo.url}</a>
          </li>
       `).join('')}
      </ul>


    `;

    reposContainer.appendChild(box);
    reposContainer.style.display = "block";

    setTimeout(() => {
      reposContainer.style.display = "none";
    }, 10000);
  }

  window.electronAPI.onDisplayAllRepos((data) => {
    console.log("Received repos:", data);
    showReposResult(data);
  });

  function showRepoContents(data) {
    if (!contentsContainer) return;

    const box = document.createElement('div');
    box.className = 'neon-box';
    box.innerHTML = `
      <p><strong>Repository:</strong> ${data.repository}</p>
      <p><strong>Contents:</strong></p>
      <ul>${data.contents.map(file => `<li>${file}</li>`).join('')}</ul>
    `;

    contentsContainer.appendChild(box);
    contentsContainer.style.display = "block";

    setTimeout(() => {
      contentsContainer.style.display = "none";
    }, 10000);
  }

  window.electronAPI.onAccessContentsOfRepo((data) => {
    console.log("Repo contents:", data);
    showRepoContents(data);
  });

  window.electronAPI.onFolderPath((data) => {
    console.log("Prompt from backend:", data.prompt);
    window.electronAPI.selectFolderPath().then((selectedPath) => {
      console.log("User selected path:", selectedPath);
      
    });
  });



  


});
