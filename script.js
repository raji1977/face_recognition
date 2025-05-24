// static/script.js

document.addEventListener("DOMContentLoaded", () => {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const captureBtn = document.getElementById("capture-btn");
    const resultText = document.getElementById("result");
    const capturedImg = document.getElementById("captured-img");

    // Access webcam
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
        })
        .catch((err) => {
            console.error("Webcam error:", err);
        });

    captureBtn.addEventListener("click", () => {
        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataURL = canvas.toDataURL("image/jpeg");

        fetch("/capture_snapshot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image: dataURL })
        })
            .then(res => res.json())
            .then(data => {
                resultText.textContent = "Recognized: " + (data.result.length ? data.result.join(', ') : "None");
                capturedImg.src = data.image_url;
                capturedImg.style.display = "block";
            })
            .catch(err => {
                console.error("Error sending image:", err);
            });
    });
});
