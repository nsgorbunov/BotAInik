const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

/**
 * Добавляем сообщение в чат, рендерим LaTeX.
 * @param {string} content - Текст (могут быть $...$ формулы).
 * @param {'user'|'bot'} sender - Кто отправил.
 * @param {boolean} isTyping - флаг, если это "анимация печати" (заглушка).
 * @returns {HTMLDivElement} - DOM-элемент сообщения
 */
function addMessage(content, sender = "user", isTyping = false) {
  // cоздаем обёртку для сообщения
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender);
  if (isTyping) {
    msgDiv.classList.add("typing");
  }

  // внутренний контейнер
  const contentDiv = document.createElement("div");
  contentDiv.classList.add("message-content");

  if (isTyping) {
    contentDiv.innerHTML = content;
  } else {
    // вставляем HTML напрямую
    contentDiv.innerHTML = content;
  }

  // всстраиваем
  msgDiv.appendChild(contentDiv);
  chatWindow.appendChild(msgDiv);

  // скроллим вниз
  chatWindow.scrollTop = chatWindow.scrollHeight;

  // ререндерим MathJax (формулы)
  if (window.MathJax && !isTyping) {
    // можно использовать typesetPromise(), чтобы дождаться завершения
    window.MathJax.typesetPromise([contentDiv]).then(() => {
      // отрендерилось
    }).catch((err) => console.error(err));
  }

  return msgDiv;
}

/** анимация печати для бота пока ждем ответ */
function showTypingIndicator() {
  const placeholderMsg = addMessage('...', 'bot', true);

  const contentDiv = placeholderMsg.querySelector('.message-content');

  // будем менять 0, 1, 2, 3 точки по кругу
  let dotCount = 1;
  const intervalId = setInterval(() => {
    dotCount = (dotCount + 1) % 4;
    // 0 => '', 1 => '.', 2 => '..', 3 => '...'
    contentDiv.textContent = '.'.repeat(dotCount);
  }, 400);

  // возвращаем объект с методами (для удаления/остановки)
  return {
    placeholderMsg,
    stop: () => clearInterval(intervalId),
  };
}

/** удаляем заглушку */
function removeTypingIndicator(typingObj) {
  if (!typingObj) return;
  typingObj.stop();  // останавливаем setInterval
  if (typingObj.placeholderMsg) {
    typingObj.placeholderMsg.remove();
  }
}

/** обработка кнопки */
sendBtn.addEventListener("click", async () => {
  const question = userInput.value.trim();
  if (!question) {
    alert("Сначала введите вопрос!");
    return;
  }

  // сообщение пользователя
  addMessage(question, "user");
  userInput.value = "";

  // "typing" от бота
  const typingObj = showTypingIndicator();

  // запрос на бэк
  try {
    const response = await fetch("/api/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    });

    // убираем заглушку когда ответ придёт
    removeTypingIndicator(typingObj);

    if (!response.ok) {
      const errorData = await response.json();
      console.error(errorData);
      addMessage("Ошибка сервера: " + (errorData.error || "Unknown"), "bot");
      return;
    }

    const data = await response.json();
    const answer = data.answer || "Нет ответа...";

    // ответ бота
    addMessage(answer, "bot");
  } catch (err) {
    removeTypingIndicator(typingObj);
    console.error(err);
    addMessage("Ошибка сети или сервера", "bot");
  }
});

userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendBtn.click();
  }
});
