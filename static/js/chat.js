$(function () {
  let socket = null;
  let currentBooking = null;

  $(document).on("click", ".open-chat", function (e) {
    e.preventDefault();
    currentBooking = $(this).data("booking-id");
    $("#chatMessages").html("");
    $("#chatModal").modal("show");

    const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    const wsUrl = ws_scheme + "://" + window.location.host + "/ws/chat/" + currentBooking + "/";
    if (socket && socket.readyState === WebSocket.OPEN) socket.close();
    socket = new WebSocket(wsUrl);

    socket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      appendMessage(data);
    };

    socket.onopen = () => console.log("Connected to chat for booking", currentBooking);
    socket.onclose = () => console.log("Chat closed");
  });

  $("#sendChatBtn").click(function () {
    const message = $("#chatInput").val().trim();
    if (!message || socket.readyState !== WebSocket.OPEN) return;
    socket.send(JSON.stringify({ message: message }));
    $("#chatInput").val("");
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
