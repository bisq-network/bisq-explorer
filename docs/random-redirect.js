var explorers = [
    "https://bsq.ninja",
    "https://bsq.sqrrm.net",
    "https://bsq.bisq.services",
    "https://bsq.vante.me",
    "https://bsq.emzy.de",
    "https://bsq.bisq.cc",
];
var explorer = explorers[Math.floor(Math.random() * 1000) % explorers.length];
document.location.href = explorer + document.location.pathname + document.location.search;
