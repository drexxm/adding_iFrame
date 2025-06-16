function loadPage(page, tabElement) {
  document.getElementById('contentFrame').src = page;

  // Toggle active class for tabs
  const tabs = document.querySelectorAll('#navTabs .nav-link');
  tabs.forEach(tab => tab.classList.remove('active'));
  tabElement.classList.add('active');
}