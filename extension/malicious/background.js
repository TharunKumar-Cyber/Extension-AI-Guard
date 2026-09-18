console.log("[Malicious Simulator] Service worker started");

const TEST_SERVER = "http://192.168.31.9:9000";

chrome.alarms.create("malicious-traffic-test", {
  periodInMinutes: 1
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name !== "malicious-traffic-test") return;

  console.log("[Malicious Simulator] Generating controlled abnormal traffic");

  const payload = {
    test_id: `mal-${Date.now()}`,
    pattern: "repeated-large-traffic",
    data: "X".repeat(10000),
    timestamp: new Date().toISOString()
  };

  fetch(`${TEST_SERVER}/malicious-test`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  })
    .then((response) => response.json())
    .then((result) => {
      console.log(
        "[Malicious Simulator] Controlled traffic sent:",
        result
      );
    })
    .catch((error) => {
      console.log(
        "[Malicious Simulator] Test request failed:",
        error.message
      );
    });
});