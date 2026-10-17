const cpuHistory = [];
const labels = [];

const ctx = document.getElementById("cpuChart");

const cpuChart = new Chart(ctx, {
    type: "line",
    data: {
        labels: labels,
        datasets: [{
            label: "CPU Usage (%)",
            data: cpuHistory,
            borderColor: "#60a5fa",
            backgroundColor: "rgba(96,165,250,0.15)",
            fill: true,
            tension: 0.3
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                min: 0,
                max: 100
            }
        }
    }
});

async function updateMetrics() {
    try {
        const response = await fetch("/api/metrics");
        if (!response.ok) throw new Error("Server unavailable");

        const data = await response.json();

        document.getElementById("cpu").textContent =
            data.cpu + "%";
        document.getElementById("memory").textContent =
            data.memory + "%";
        document.getElementById("disk").textContent =
            data.disk + "%";
        document.getElementById("status").textContent = "Online";
        document.getElementById("updated").textContent =
            "Last updated: " + new Date().toLocaleTimeString();

        labels.push(new Date().toLocaleTimeString());
        cpuHistory.push(data.cpu);

        if (labels.length > 10) {
            labels.shift();
            cpuHistory.shift();
        }

        cpuChart.update();
    } catch (error) {
        document.getElementById("status").textContent = "Offline";
        document.getElementById("updated").textContent =
            "Unable to retrieve server metrics.";
    }
}

updateMetrics();
setInterval(updateMetrics, 5000);
