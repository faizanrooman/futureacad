/* ============================================================
   FutureAcad — Contact form submission (contact page)
   Posts JSON to /api/contact with CSRF token, inline feedback.
   ============================================================ */
(function () {
  'use strict';
  const form = document.getElementById('contactForm');
  if (!form) return;
  const status = document.getElementById('formStatus');
  const btn = form.querySelector('button[type="submit"]');

  function setStatus(msg, kind) {
    status.textContent = msg;
    status.className = 'form__status' + (kind ? ' form__status--' + kind : '');
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    // Honeypot — bots fill this hidden field; humans never see it.
    if (form.querySelector('[name="company_website"]').value) return;

    const data = {
      name: form.name.value.trim(),
      email: form.email.value.trim(),
      company: form.company.value.trim(),
      interest: form.interest.value,
      message: form.message.value.trim(),
    };

    if (!data.name || !data.email || !data.message) {
      setStatus('Please fill in your name, email, and message.', 'error');
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
      setStatus('That email address doesn’t look right.', 'error');
      return;
    }

    btn.disabled = true;
    const label = btn.querySelector('span');
    const original = label ? label.textContent : '';
    if (label) label.textContent = 'Sending…';
    setStatus('', '');

    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': form.dataset.csrf || '' },
        body: JSON.stringify(data),
      });
      const json = await res.json().catch(() => ({}));
      if (res.ok && json.ok) {
        form.reset();
        setStatus('Thank you — your message is in. We’ll be in touch shortly.', 'ok');
        form.classList.add('is-sent');
      } else {
        setStatus(json.error || 'Something went wrong. Please try again.', 'error');
      }
    } catch (err) {
      setStatus('Network error. Please check your connection and retry.', 'error');
    } finally {
      btn.disabled = false;
      if (label) label.textContent = original;
    }
  });
})();
