// NEXOVERSE interactions
// Edit this file to change navigation and enquiry-form behavior.

const menuBtn = document.getElementById("menuBtn");
const navLinks = document.getElementById("navLinks");
const enquiryForm = document.getElementById("enquiryForm");
const formNote = document.getElementById("formNote");

const CONTACT_EMAIL = "priyanshsaxena43@gmail.com";
const WHATSAPP_NUMBER = "91852884381";

if (menuBtn && navLinks) {
  menuBtn.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("active");
    menuBtn.setAttribute("aria-expanded", String(isOpen));
    menuBtn.setAttribute("aria-label", isOpen ? "Close navigation" : "Open navigation");
    menuBtn.textContent = isOpen ? "×" : "☰";
  });

  navLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("active");
      menuBtn.setAttribute("aria-expanded", "false");
      menuBtn.setAttribute("aria-label", "Open navigation");
      menuBtn.textContent = "☰";
    });
  });
}

if (enquiryForm) {
  enquiryForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!enquiryForm.reportValidity()) return;

    const submitButton = enquiryForm.querySelector('button[type="submit"]');
    const formData = new FormData(enquiryForm);
    const enquiry = {
      name: String(formData.get("name")).trim(),
      email: String(formData.get("email")).trim(),
      service: String(formData.get("service")).trim(),
      message: String(formData.get("message")).trim()
    };

    if (submitButton) submitButton.disabled = true;
    if (formNote) formNote.textContent = "Submitting your enquiry...";

    try {
      const response = await fetch("/api/enquiries", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(enquiry)
      });

      const result = await response.json();
      if (!response.ok) throw new Error(result.detail || "Submission failed.");

      enquiryForm.reset();
      if (formNote) formNote.textContent = "Thank you! Your enquiry has been saved. We will contact you soon.";
    } catch (error) {
      if (formNote) formNote.textContent = error.message || "Could not submit your enquiry. Please try again.";
    } finally {
      if (submitButton) submitButton.disabled = false;
    }
  });
}

const yearElement = document.getElementById("year");
if (yearElement) {
  yearElement.textContent = new Date().getFullYear();
}

// Keep the WhatsApp number in one place for future links added via JavaScript.
document.querySelectorAll('a[href*="wa.me"]').forEach((link) => {
  link.setAttribute("href", link.getAttribute("href").replace("91852884381", WHATSAPP_NUMBER));
});
