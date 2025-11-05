document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('header');
  const onScroll = () => {
    if (window.scrollY > 4) header.classList.add('border-white/10');
    else header.classList.remove('border-white/10');
  };
  document.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
});


