

export function initializeModal(modalId, openSelector = '.modal-opener', closeSelector = '.modal-closer') {
  const modal = document.getElementById(modalId);
  (document.querySelectorAll(openSelector) || []).forEach((modalOpener) => {
    modalOpener.addEventListener('click', () => {
      modal.classList.add('is-active');
    })
  });
  (document.querySelectorAll(closeSelector) || []).forEach((modalCloser) => {
    modalCloser.addEventListener('click', () => {
      modal.classList.remove('is-active');
    });
  });
}

export const Modals = {
  initializeModal,
};
