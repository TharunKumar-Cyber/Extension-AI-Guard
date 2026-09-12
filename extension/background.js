const TEST_SERVER = "http://127.0.0.1:9000";

chrome.webRequest.onBeforeRequest.addListener(
  (details) => {
    console.log("[Extension AI Guard]", {
      url: details.url,
      method: details.method,
      type: details.type
    });
  },
  { urls: ["<all_urls>"] }
);

chrome.alarms.create("safe-traffic-test", {
  periodInMinutes: 1
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name !== "safe-traffic-test") return;

  fetch(`${TEST_SERVER}/safe`)
    .then(() => {
      console.log("[Extension AI Guard] Controlled safe traffic generated");
    })
    .catch((error) => {
      console.log(
        "[Extension AI Guard] Safe traffic request failed:",
        error.message
      );
    });
});