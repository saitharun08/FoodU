$(function () {
  let socket = null;
  let currentBooking = null;

  $(document).on("click", ".open-chat", function (e) {
    e.preventDefault();
    currentBooking = $(this).data("booking-id");
    $("#chatMessages").html("");
    // Use Bootstrap 5 modal API
    const chatModal = new bootstrap.Modal(document.getElementById('chatModal'));
    chatModal.show();

    const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    const wsUrl = ws_scheme + "://" + window.location.host + "/ws/chat/" + currentBooking + "/";
    if (socket && socket.readyState === WebSocket.OPEN) socket.close();
    socket = new WebSocket(wsUrl);

    socket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      appendMessage(data);
    };

    socket.onopen = () => console.log("Connected to chat for booking", currentBooking);
    socket.onclose = (event) => {
      console.log("Chat closed", event.code, event.reason);
      if (event.code !== 1000) {
        alert("Chat connection closed. Please make sure the order is assigned to a partner.");
      }
    };
    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
      alert("Failed to connect to chat. Please refresh the page and try again.");
    };
  });

  $("#sendChatBtn").click(function () {
    const message = $("#chatInput").val().trim();
    if (!message || socket.readyState !== WebSocket.OPEN) return;
    socket.send(JSON.stringify({ message: message }));
    $("#chatInput").val("");
  });

  // Allow Enter key to send message
  $("#chatInput").keypress(function (e) {
    if (e.which === 13) { // Enter key
      $("#sendChatBtn").click();
    }
  });

  function appendMessage(data) {
    const me = $("#userMobile").val();
    const align = data.sender_mobile === me ? "text-end" : "text-start";
    const html = `
      <div class="${align}">
        <strong>${data.sender_mobile}</strong><br>
        ${data.message}<br>
        <small class="text-muted">${new Date().toLocaleTimeString()}</small>
        <hr>
      </div>`;
    $("#chatMessages").append(html);
    $("#chatMessages").scrollTop($("#chatMessages")[0].scrollHeight);
  }
});
