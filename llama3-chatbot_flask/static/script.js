document.addEventListener('DOMContentLoaded', function() {
    const eventSource = new EventSource('/stream');
   
    eventSource.onmessage = function(event) {
        document.getElementById('datetime').innerHTML = event.data;
    };
   
    const status_txt = document.getElementById('status_txt');
   
    document.getElementById('GO').addEventListener('click', () => {
        status_txt.textContent = "Loading...";
        loading_animate.style.display = "flex";
    });
});
