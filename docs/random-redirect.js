var explorers = [
    "https://bsq.ninja",
    "https://bsq.emzy.de",
    "https://bsq.bisq.services"
];
var explorer = explorers[Math.floor(Math.random() * 1000) % explorers.length];
document.location.href = explorer + document.location.pathname + document.location.search;
