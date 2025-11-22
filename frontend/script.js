async function sendURL() {
  const url = document.getElementById("urlInput").value;
  
  if (!url) {
    document.getElementById("result").innerHTML = "❌ Please enter a URL";
    return;
  }

  try {
    document.getElementById("result").innerHTML = "⏳ Scanning...";
    
    const response = await axios.post("http://localhost:5000/predict", {
      url: url
    });

    const result = response.data;
    const isMalicious = result.prediction === 1;

    document.getElementById("result").innerHTML = `
      <div class="result-card ${isMalicious ? 'malicious' : 'safe'}">
        <h3>${isMalicious ? "🔴 Malicious" : "🟢 Safe"}</h3>
        <p><strong>Confidence:</strong> ${result.confidence.toFixed(2)}%</p>
        <p><strong>Method:</strong> ${result.method}</p>
        <p><strong>Message:</strong> ${result.message}</p>
        <small>URL: ${result.url}</small>
      </div>
      <button onclick="reportFeedback()" class="feedback-btn">
        📋 Report this result
      </button>
    `;

  } catch (error) {
    console.error("❌ Error:", error);
    document.getElementById("result").innerHTML = `
      <div class="error">
        ❌ Error: Couldn't reach the backend. Make sure the server is running on port 5000.
      </div>
    `;
  }
}

async function reportFeedback() {
  const url = document.getElementById("urlInput").value;
  const userClassification = prompt("Should this be Safe (0) or Malicious (1)?");
  
  if (userClassification !== null) {
    try {
      await axios.post('http://localhost:5000/feedback', {
        url: url,
        expected_class: parseInt(userClassification)
      });
      alert("✅ Thanks for improving our model!");
    } catch (error) {
      alert("❌ Error submitting feedback");
    }
  }
}
