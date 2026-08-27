/* Gallery lightbox. Progressive enhancement: without JS the thumbnails are
   still images with captions, they just don't enlarge. */
(function () {
  var box = document.getElementById("lightbox");
  if (!box) return;
  var img = document.getElementById("lightbox-img");
  var cap = document.getElementById("lightbox-cap");
  var closeBtn = document.getElementById("lightbox-close");
  var lastFocus = null;

  function open(btn) {
    lastFocus = btn;
    img.src = btn.getAttribute("data-full");
    img.alt = btn.querySelector("img").alt;
    cap.innerHTML = btn.getAttribute("data-cap") || "";
    box.hidden = false;
    document.body.style.overflow = "hidden";
    closeBtn.focus();
  }

  function close() {
    box.hidden = true;
    img.src = "";
    document.body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }

  document.querySelectorAll(".gal__btn").forEach(function (b) {
    b.addEventListener("click", function () { open(b); });
  });
  closeBtn.addEventListener("click", close);
  box.addEventListener("click", function (e) { if (e.target === box) close(); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !box.hidden) close();
  });
})();
