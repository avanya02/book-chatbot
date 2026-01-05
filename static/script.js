async function sendPrompt() {
  const prompt = document.getElementById("prompt").value;
  const responseBox = document.getElementById("response");

  if (!prompt.trim()) {
    responseBox.innerText = "Please enter a question 🙂";
    return;
  }

  responseBox.innerText = "Thinking... 🤔";

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ query: prompt })
    });

    const data = await res.json();
    responseBox.innerText = data.answer;
  } catch (err) {
    responseBox.innerText = "Something went wrong 😢";
  }
}
