$(function () {
  let socket = null;
  let currentBooking = null;

  // open chat modal
  $(document).on("click", ".open-chat", function (e) {
    e.preventDefault();
    currentBooking = $(this).data("booking-id");

    $("#chatBookingId").text(currentBooking);
    $("#chatMessages").html("");
    $("#chatModal").modal("show");

    // determine ws/wss scheme
    const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    const wsUrl = ws_scheme + "://" + window.location.host + "/ws/chat/" + currentBooking + "/";

    // close previous connection if open
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.close();
    }

    // open a new WebSocket
    socket = new WebSocket(wsUrl);

    socket.onopen = function () {
      console.log("🔌 WebSocket connected for booking", currentBooking);
      // fetch previous chat history (optional)
      fetchMessages(currentBooking);
    };

    socket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      appendMessage(data);
    };

    socket.onclose = function () {
      console.log("⚠️ WebSocket closed");
    };

    socket.onerror = function (error) {
      console.error("❌ WebSocket error:", error);
    };
  });

  // send message
  $("#sendChatBtn").click(function () {
    const message = $("#chatInput").val().trim();
    if (!message || !socket || socket.readyState !== WebSocket.OPEN) return;
    socket.send(JSON.stringify({ message: message }));
    $("#chatInput").val("");
  });

  // helper: render a message
  function appendMessage(data) {
    const meMobile = $("#userMobile").val(); // hidden input with current user's mobile
    const isMe = data.sender_mobile === meMobile;
    const alignment = isMe ? "text-end" : "text-start";
    const html = `
      <div class="${alignment}">
        <div><strong>${data.sender_mobile}</strong></div>
        <div>${data.message}</div>
        <small class="text-muted">${new Date(data.timestamp).toLocaleTimeString()}</small>
        <hr/>
      </div>`;
    $("#chatMessages").append(html);
    $("#chatMessages").scrollTop($("#chatMessages")[0].scrollHeight);
  }

  // optional: load previous messages via AJAX
  function fetchMessages(bookingId) {
    $.get(`/chat/history/${bookingId}/`, function (resp) {
      resp.messages.forEach((m) => appendMessage(m));
    });
  }
});
