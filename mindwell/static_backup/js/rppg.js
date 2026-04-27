document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('videoElement');
    const startBtn = document.getElementById('startBtn');
    const overlay = document.getElementById('scanOverlay');
    const progressSpan = document.getElementById('progress');
    const resultsArea = document.getElementById('resultsArea');
    const hrValue = document.getElementById('hrValue');
    const stressValue = document.getElementById('stressValue');

    let stream = null;

    startBtn.addEventListener('click', async () => {
        if (!stream) {
            try {
                stream = await navigator.mediaDevices.getUserMedia({ video: true });
                video.srcObject = stream;
                startBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Scan';
                startAnalysis();
            } catch (err) {
                alert("Could not access camera: " + err);
            }
        } else {
            stopScan();
        }
    });

    function startAnalysis() {
        overlay.style.display = 'block';
        resultsArea.style.display = 'none';
        
        let progress = 0;
        const interval = setInterval(() => {
            progress += 5;
            progressSpan.textContent = progress + '%';
            
            if (progress >= 100) {
                clearInterval(interval);
                completeScan();
            }
        }, 200); // 4 seconds total scan time
    }

    function completeScan() {
        overlay.style.display = 'none';
        resultsArea.style.display = 'flex';
        
        // Mock Results (Simulation of rPPG)
        const mockHR = Math.floor(Math.random() * (90 - 60) + 60);
        const mockStress = Math.random() > 0.5 ? "Low" : "Moderate";
        
        hrValue.textContent = mockHR;
        stressValue.textContent = mockStress;
        
        // Change color based on stress
        if (mockStress === "Moderate" || mockStress === "High") {
            stressValue.style.color = "#FFCC00";
        } else {
            stressValue.style.color = "#4CD964";
        }

        startBtn.innerHTML = '<i class="fas fa-redo"></i> Scan Again';
    }

    function stopScan() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            video.srcObject = null;
            stream = null;
        }
        startBtn.innerHTML = '<i class="fas fa-camera"></i> Start Scan';
        overlay.style.display = 'none';
    }
});
