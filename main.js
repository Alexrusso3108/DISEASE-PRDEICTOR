import './style.css'

document.addEventListener('DOMContentLoaded', () => {
  // Navigation Logic
  const navLinks = document.querySelectorAll('.nav-link');
  const pages = document.querySelectorAll('.page');

  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      
      // Remove active class from all links and pages
      navLinks.forEach(l => l.classList.remove('active'));
      pages.forEach(p => p.classList.remove('active'));
      
      // Add active class to clicked link
      link.classList.add('active');
      
      // Show corresponding page
      const targetId = link.getAttribute('data-target');
      const targetPage = document.getElementById(targetId);
      if(targetPage) {
        targetPage.classList.add('active');
      }
    });
  });

  // Predictor Logic (Mock AI Scan)
  const form = document.getElementById('prediction-form');
  const idleState = document.querySelector('.idle-state');
  const scanningState = document.querySelector('.scanning-state');
  const resultState = document.querySelector('.result-state');
  const progressFill = document.querySelector('.progress-fill');
  const resetBtn = document.getElementById('reset-btn');

  if(form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      
      // Hide idle and show scanning
      idleState.classList.add('hidden');
      resultState.classList.add('hidden');
      scanningState.classList.remove('hidden');
      
      // Animate progress bar
      let progress = 0;
      progressFill.style.width = '0%';
      
      const interval = setInterval(() => {
        progress += Math.random() * 15;
        if(progress > 100) progress = 100;
        
        progressFill.style.width = `${progress}%`;
        
        if(progress === 100) {
          clearInterval(interval);
          setTimeout(() => {
            // Show result
            scanningState.classList.add('hidden');
            resultState.classList.remove('hidden');
          }, 500);
        }
      }, 300);
    });
  }

  if(resetBtn) {
    resetBtn.addEventListener('click', () => {
      form.reset();
      resultState.classList.add('hidden');
      idleState.classList.remove('hidden');
    });
  }
});
