//Why was this file created???
//Why did I do this???
//I don't know...
//
//Is there some use for this... hmmm...

// Home page functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Home page loaded');
    
    // Add a welcome message to the page
    const container = document.querySelector('.container');
    const welcomeMsg = document.createElement('p');
    welcomeMsg.textContent = 'Welcome to our application! This is a simple home page.';
    welcomeMsg.style.marginTop = '20px';
    container.appendChild(welcomeMsg);
    
    // Add a timestamp to show when the page was loaded
    const timestamp = document.createElement('p');
    timestamp.textContent = `Page loaded at: ${new Date().toLocaleString()}`;
    timestamp.style.fontSize = '0.8em';
    timestamp.style.color = '#666';
    container.appendChild(timestamp);
});