// Content script - runs on every webpage
console.log('Sahayak content script loaded');

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'execute') {
    executeAction(request.data)
      .then(result => sendResponse({ success: true, result }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep channel open for async response
  }
  
  if (request.action === 'capture') {
    captureScreenshot()
      .then(screenshot => sendResponse({ success: true, screenshot }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }
  
  if (request.action === 'highlight') {
    highlightElement(request.selector);
    sendResponse({ success: true });
  }
});

// Execute automation action
async function executeAction(actionData) {
  const { action, selector, value } = actionData;
  
  console.log('Executing action:', action, selector, value);
  
  try {
    switch (action) {
      case 'type':
        return await typeText(selector, value);
      
      case 'click':
        return await clickElement(selector);
      
      case 'scroll':
        return await scrollPage(value);
      
      case 'wait':
        return await wait(parseInt(value) * 1000);
      
      default:
        throw new Error(`Unknown action: ${action}`);
    }
  } catch (error) {
    console.error('Action execution failed:', error);
    throw error;
  }
}

// Type text into element
async function typeText(selector, text) {
  const element = findElement(selector);
  
  if (!element) {
    throw new Error(`Element not found: ${selector}`);
  }
  
  if (!element.matches('input, textarea')) {
    throw new Error('Element is not an input or textarea');
  }
  
  // Highlight element
  highlightElement(selector);
  
  // Clear existing value
  element.value = '';
  
  // Simulate typing with delay
  for (let i = 0; i < text.length; i++) {
    await wait(50); // 50ms delay between characters
    element.value += text[i];
    
    // Trigger input event
    element.dispatchEvent(new Event('input', { bubbles: true }));
  }
  
  // Trigger change event
  element.dispatchEvent(new Event('change', { bubbles: true }));
  
  return { element: selector, value: text };
}

// Click element
async function clickElement(selector) {
  const element = findElement(selector);
  
  if (!element) {
    throw new Error(`Element not found: ${selector}`);
  }
  
  // Highlight element
  highlightElement(selector);
  
  await wait(300);
  
  // Scroll into view
  element.scrollIntoView({ behavior: 'smooth', block: 'center' });
  
  await wait(300);
  
  // Click
  element.click();
  
  return { element: selector, clicked: true };
}

// Scroll page
async function scrollPage(direction) {
  const scrollAmount = window.innerHeight * 0.8;
  
  if (direction === 'up') {
    window.scrollBy({ top: -scrollAmount, behavior: 'smooth' });
  } else {
    window.scrollBy({ top: scrollAmount, behavior: 'smooth' });
  }
  
  return { scrolled: direction, amount: scrollAmount };
}

// Wait for specified duration
function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Find element using various strategies
function findElement(selector) {
  try {
    // Try direct selector
    let element = document.querySelector(selector);
    if (element) return element;
    
    // Try with case-insensitive attribute matching
    const attributes = ['name', 'id', 'placeholder', 'aria-label'];
    
    for (const attr of attributes) {
      const match = selector.match(new RegExp(`${attr}\\*?=['"]([^'"]+)['"]`, 'i'));
      if (match) {
        const value = match[1].toLowerCase();
        element = Array.from(document.querySelectorAll(`[${attr}]`))
          .find(el => el.getAttribute(attr).toLowerCase().includes(value));
        if (element) return element;
      }
    }
    
    // Try text content matching
    const textMatch = selector.match(/:contains\(['"]([^'"]+)['"]\)/i);
    if (textMatch) {
      const text = textMatch[1].toLowerCase();
      element = Array.from(document.querySelectorAll('button, a, span, div'))
        .find(el => el.textContent.toLowerCase().includes(text));
      if (element) return element;
    }
    
    return null;
  } catch (error) {
    console.error('Error finding element:', error);
    return null;
  }
}

// Highlight element
function highlightElement(selector) {
  const element = findElement(selector);
  if (!element) return;
  
  // Remove existing highlights
  document.querySelectorAll('.sahayak-highlight').forEach(el => {
    el.classList.remove('sahayak-highlight');
  });
  
  // Add highlight
  element.classList.add('sahayak-highlight');
  
  // Add highlight styles if not already added
  if (!document.getElementById('sahayak-highlight-styles')) {
    const style = document.createElement('style');
    style.id = 'sahayak-highlight-styles';
    style.textContent = `
      .sahayak-highlight {
        outline: 3px solid #00f0ff !important;
        outline-offset: 2px !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.5) !important;
        animation: sahayak-pulse 1s ease-in-out 3;
      }
      
      @keyframes sahayak-pulse {
        0%, 100% { outline-color: #00f0ff; }
        50% { outline-color: #ff006e; }
      }
    `;
    document.head.appendChild(style);
  }
  
  // Remove highlight after 3 seconds
  setTimeout(() => {
    element.classList.remove('sahayak-highlight');
  }, 3000);
}

// Capture screenshot
async function captureScreenshot() {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendMessage(
      { action: 'captureTab' },
      response => {
        if (response && response.screenshot) {
          resolve(response.screenshot);
        } else {
          reject(new Error('Failed to capture screenshot'));
        }
      }
    );
  });
}

// Inject helper for page analysis
window.sahayakHelper = {
  getPageInfo: () => {
    return {
      title: document.title,
      url: window.location.href,
      forms: Array.from(document.querySelectorAll('form')).map(form => ({
        id: form.id,
        action: form.action,
        inputs: Array.from(form.querySelectorAll('input, textarea, select')).map(input => ({
          type: input.type,
          name: input.name,
          id: input.id,
          placeholder: input.placeholder
        }))
      })),
      buttons: Array.from(document.querySelectorAll('button, input[type="submit"]')).map(btn => ({
        text: btn.textContent || btn.value,
        type: btn.type,
        id: btn.id
      }))
    };
  }
};