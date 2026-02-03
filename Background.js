// Background service worker
console.log('Sahayak background service worker loaded');

// Handle screenshot capture
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'captureTab') {
    chrome.tabs.captureVisibleTab(
      null,
      { format: 'png' },
      (dataUrl) => {
        if (chrome.runtime.lastError) {
          console.error('Capture error:', chrome.runtime.lastError);
          sendResponse({ success: false, error: chrome.runtime.lastError.message });
        } else {
          // Convert to base64
          const base64 = dataUrl.split(',')[1];
          sendResponse({ success: true, screenshot: base64 });
        }
      }
    );
    return true; // Keep channel open for async response
  }
  
  if (request.action === 'executeOnTab') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        chrome.tabs.sendMessage(
          tabs[0].id,
          { action: 'execute', data: request.data },
          (response) => {
            sendResponse(response);
          }
        );
      }
    });
    return true;
  }
});

// Handle installation
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('Sahayak installed successfully');
    
    // Open welcome page
    chrome.tabs.create({
      url: chrome.runtime.getURL('popup.html')
    });
  }
});

// Context menu for quick actions
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'sahayak-automate',
    title: 'Automate with Sahayak',
    contexts: ['page']
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'sahayak-automate') {
    chrome.action.openPopup();
  }
});

// Storage helpers
const storage = {
  async get(key) {
    return new Promise((resolve) => {
      chrome.storage.local.get([key], (result) => {
        resolve(result[key]);
      });
    });
  },
  
  async set(key, value) {
    return new Promise((resolve) => {
      chrome.storage.local.set({ [key]: value }, resolve);
    });
  },
  
  async remove(key) {
    return new Promise((resolve) => {
      chrome.storage.local.remove([key], resolve);
    });
  }
};

// Store action history
async function storeAction(action) {
  const history = await storage.get('actionHistory') || [];
  history.unshift({
    ...action,
    timestamp: new Date().toISOString()
  });
  
  // Keep only last 100 actions
  if (history.length > 100) {
    history.pop();
  }
  
  await storage.set('actionHistory', history);
}

// Export storage helper
chrome.runtime.storage = storage;
chrome.runtime.storeAction = storeAction;