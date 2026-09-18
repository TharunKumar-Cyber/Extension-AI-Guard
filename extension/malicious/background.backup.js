console.log("[Malicious Simulator] Service worker started");

const TEST_SERVER = "http://127.0.0.1:8000";

chrome.alarms.create("traffic-test", {
  periodInMinutes: 1
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name !== "traffic-test") return;

  console.log("[Malicious Simulator] Generating controlled test traffic");

  fetch(`${TEST_SERVER}/api/network-requests`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      request_id: `sim-${Date.now()}`,
      url: "http://127.0.0.1:8000/simulated/suspicious",
      domain: "simulated-malware.local",
      method: "POST",
      timestamp: new Date().toISOString()
    })
  }).catch((error) => {
    console.log("[Malicious Simulator] Test request failed:", error.message);
  });
});
