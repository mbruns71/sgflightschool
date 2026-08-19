/* Booking form: progressive enhancement.
   Without JS the form still POSTs normally to /api/book and the visitor gets a
   JSON response — ugly but functional. With JS they stay on the page and get
   inline errors. */
(function () {
  var form = document.getElementById("book-form");
  if (!form) return;

  var btn = document.getElementById("book-submit");
  var status = document.getElementById("book-status");
  var original = btn.innerHTML;

  function clearErrors() {
    form.querySelectorAll(".field-error").forEach(function (e) { e.remove(); });
    form.querySelectorAll("[aria-invalid]").forEach(function (e) {
      e.removeAttribute("aria-invalid");
    });
  }

  function showError(field, message) {
    var input = form.elements[field];
    if (!input) return;
    input.setAttribute("aria-invalid", "true");
    var p = document.createElement("p");
    p.className = "field-error";
    p.textContent = message;
    input.parentNode.appendChild(p);
  }

  function setStatus(state, message) {
    status.setAttribute("data-state", state);
    status.textContent = message;
  }

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    clearErrors();
    setStatus("", "");

    btn.disabled = true;
    btn.innerHTML = "Sending…";

    var payload = {};
    ["name", "phone", "email", "interest", "when", "notes", "website"].forEach(
      function (f) {
        var el = form.elements[f];
        if (el) payload[f] = el.value;
      }
    );

    fetch(form.action, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then(function (res) {
        return res.json().then(function (body) {
          return { status: res.status, body: body };
        });
      })
      .then(function (r) {
        if (r.status === 422 && r.body.errors) {
          Object.keys(r.body.errors).forEach(function (f) {
            showError(f, r.body.errors[f]);
          });
          setStatus("err", "Please check the highlighted fields.");
          var first = form.querySelector('[aria-invalid="true"]');
          if (first) first.focus();
          return;
        }
        if (!r.body.ok) {
          throw new Error(r.body.error || "request failed");
        }
        form.querySelectorAll("input, select, textarea").forEach(function (e) {
          e.disabled = true;
        });
        btn.remove();
        setStatus("ok", r.body.message || "Thanks — we've got it.");
        status.scrollIntoView({ behavior: "smooth", block: "center" });
      })
      .catch(function () {
        setStatus(
          "err",
          "Sorry — something went wrong sending that. Please call (406) 609-6798 " +
            "or email info@sgflightschool.com and we'll get you booked."
        );
      })
      .finally(function () {
        if (document.body.contains(btn)) {
          btn.disabled = false;
          btn.innerHTML = original;
        }
      });
  });
})();
