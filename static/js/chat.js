$(function () {
  let socket = null;
  let currentBooking = null;
  let renderedMessageIds = new Set();

  $(document).on("click", ".open-chat", function (e) {
    e.preventDefault();
    const bookingId = $(this).data("booking-id");
    if (!bookingId) {
      console.warn("Booking id missing for chat button");
      return;
    }

    currentBooking = bookingId;
    renderedMessageIds = new Set();

    const chatMessagesEl = $("#chatMessages");
    chatMessagesEl.empty();
    updateChatInputState(false);

    const chatModalEl = document.getElementById("chatModal");
    if (!chatModalEl) {
      console.error("Chat modal element not found");
      return;
    }
    const chatModal = bootstrap.Modal.getOrCreateInstance(chatModalEl);
    chatModal.show();

    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.close(1000, "Switching chat session");
    }

    loadChatHistory(bookingId).always(function () {
      connectToChat(bookingId);
    });
  });

  function connectToChat(bookingId) {
    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    const wsUrl = wsScheme + "://" + window.location.host + "/ws/chat/" + bookingId + "/";
    socket = new WebSocket(wsUrl);

    socket.onopen = function () {
      console.log("Connected to chat for booking", bookingId);
      updateChatInputState(true);
    };

    socket.onmessage = function (e) {
      try {
        const data = JSON.parse(e.data);
        appendMessage(data);
      } catch (err) {
        console.error("Failed to parse chat message", err);
      }
    };

    socket.onclose = function (event) {
      console.log("Chat closed", event.code, event.reason);
      updateChatInputState(false);
      if (event.code !== 1000 && currentBooking === bookingId) {
        showAlert("Chat connection closed. Please make sure the order is assigned to a partner.");
      }
      socket = null;
    };

    socket.onerror = function (error) {
      console.error("WebSocket error:", error);
      updateChatInputState(false);
      showAlert("Failed to connect to chat. Please refresh the page and try again.");
    };
  }

  function loadChatHistory(bookingId) {
    return $.get("/chat/history/" + bookingId + "/")
      .done(function (res) {
        const messages = res && Array.isArray(res.messages) ? res.messages : [];
        messages.forEach(function (message) {
          appendMessage(message);
        });
      })
      .fail(function () {
        appendSystemMessage("Unable to load previous messages.");
      });
  }

  function updateChatInputState(enabled) {
    $("#sendChatBtn").prop("disabled", !enabled);
    $("#chatInput").prop("disabled", !enabled);
  }

  function showAlert(message) {
    window.alert(message);
  }

  function appendSystemMessage(text) {
    const chatMessagesEl = $("#chatMessages");
    if (!chatMessagesEl.length) {
      return;
    }
    const container = $("<div>").addClass("text-center text-muted").text(text);
    chatMessagesEl.append(container);
  }

  $("#sendChatBtn").on("click", function () {
    const message = $("#chatInput").val().trim();
    if (!message || !socket || socket.readyState !== WebSocket.OPEN) {
      return;
    }
    socket.send(JSON.stringify({ message }));
    $("#chatInput").val("");
  });

  $("#chatInput").on("keypress", function (e) {
    if (e.which === 13) {
      e.preventDefault();
      $("#sendChatBtn").trigger("click");
    }
  });

  function appendMessage(data) {
    const chatMessagesEl = $("#chatMessages");
    if (!data || !chatMessagesEl.length) {
      return;
    }

    if (data.id && renderedMessageIds.has(data.id)) {
      return;
    }
    if (data.id) {
      renderedMessageIds.add(data.id);
    }

    const me = $("#userMobile").val();
    const align = data.sender_mobile === me ? "text-end" : "text-start";

    const container = $("<div>").addClass(align);
    container.append($("<strong>").text(data.sender_mobile));
    container.append("<br>");
    container.append($("<span>").text(data.message));
    container.append("<br>");
    container.append($("<small>").addClass("text-muted").text(formatTimestamp(data.timestamp)));
    container.append($("<hr>"));

    chatMessagesEl.append(container);
    chatMessagesEl.scrollTop(chatMessagesEl[0].scrollHeight);
  }

  function formatTimestamp(timestamp) {
    if (!timestamp) {
      return new Date().toLocaleString();
    }
    const date = new Date(timestamp);
    if (Number.isNaN(date.getTime())) {
      return new Date().toLocaleString();
    }
    return date.toLocaleString();
  }
});
