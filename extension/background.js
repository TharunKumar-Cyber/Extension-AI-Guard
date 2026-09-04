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
