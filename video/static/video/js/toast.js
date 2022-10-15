function createToast(text) {
    const element = document.getElementById("toast");
    element.className = "show";
    element.innerHTML = text;
    setTimeout(function(){ element.className = element.className.replace("show", ""); }, 3000);
}