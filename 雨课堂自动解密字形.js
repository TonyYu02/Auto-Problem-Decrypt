// ==UserScript==
// @name         雨课堂自动解密字形
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  支持单页应用无刷新切换页面，自动捕获最新字体并解密
// @author       TonyYu
// @match        *://*.yuketang.cn/*
// @match        *://*.xuetangx.com/*
// @grant        GM_xmlhttpRequest
// @connect      127.0.0.1
// ==/UserScript==

(function() {
    'use strict';

    let ttfUrlCache = null;
    let decryptingNodes = new WeakSet();
    const urlRegex = /(https:\/\/[^"'\s\)]*fe_font\/product\/exam_font_[a-zA-Z0-9_-]+\.ttf)/i;
    let pollInterval = null;

    let currentUrl = location.href;
    setInterval(() => {
        if (location.href !== currentUrl) {
            currentUrl = location.href;
            ttfUrlCache = null;
            decryptingNodes = new WeakSet();
            startFontPolling();
        }
    }, 500);

    function extractFontUrl() {
        let styleTags = document.querySelectorAll('style');
        for (let i = styleTags.length - 1; i >= 0; i--) {
            let match = styleTags[i].innerHTML.match(urlRegex);
            if (match && match[1]) return match[1];
        }

        let sheets = document.styleSheets;
        for (let i = sheets.length - 1; i >= 0; i--) {
            try {
                let rules = sheets[i].cssRules;
                if (!rules) continue;
                for (let j = rules.length - 1; j >= 0; j--) {
                    if (rules[j].cssText && rules[j].cssText.match(urlRegex)) {
                        return rules[j].cssText.match(urlRegex)[1];
                    }
                }
            } catch(e) {}
        }
        return null;
    }

    function doDecryptRequest(span) {
        let encryptedText = span.innerHTML;
        GM_xmlhttpRequest({
            method: 'POST',
            url: 'http://127.0.0.1:5000/decrypt',
            headers: { 'Content-Type': 'application/json' },
            data: JSON.stringify({
                ttf_url: ttfUrlCache,
                text: `<span class="xuetangx-com-encrypted-font">${encryptedText}</span>`
            }),
            onload: function(response) {
                try {
                    let data = JSON.parse(response.responseText);
                    if (data.decrypted_text) {
                        span.innerHTML = data.decrypted_text;
                        span.classList.remove('xuetangx-com-encrypted-font');
                    }
                } catch(e) {
                    console.error("解密响应解析失败", e);
                    decryptingNodes.delete(span);
                }
            },
            onerror: function(err) {
                console.error("请求解密服务失败", err);
                decryptingNodes.delete(span);
            }
        });
    }

    function scanAndDecrypt() {
        if (!ttfUrlCache) return;

        let spans = document.querySelectorAll('.xuetangx-com-encrypted-font');
        spans.forEach(span => {
            if (decryptingNodes.has(span)) return;
            decryptingNodes.add(span);
            doDecryptRequest(span);
        });
    }

    function startFontPolling() {
        if (pollInterval) clearInterval(pollInterval);

        pollInterval = setInterval(() => {
            let url = extractFontUrl();
            if (url) {
                if (url !== ttfUrlCache) {
                    ttfUrlCache = url;
                }
                clearInterval(pollInterval);
                scanAndDecrypt();
            }
        }, 500);
    }

    // 5. 监听动态变动
    const observer = new MutationObserver((mutations) => {
        let hasNewSpans = false;

        for (let mutation of mutations) {
            for (let node of mutation.addedNodes) {
                if (node.nodeType === 1) {
                    if (node.nodeName === 'STYLE') {
                        let match = node.innerHTML.match(urlRegex);
                        if (match && match[1] && match[1] !== ttfUrlCache) {
                            ttfUrlCache = match[1];
                            hasNewSpans = true;
                        }
                    }

                    if (node.classList && node.classList.contains('xuetangx-com-encrypted-font')) {
                        hasNewSpans = true;
                    } else if (node.querySelector && node.querySelector('.xuetangx-com-encrypted-font')) {
                        hasNewSpans = true;
                    }
                }
            }
        }

        if (hasNewSpans && ttfUrlCache) {
            scanAndDecrypt();
        }
    });

    startFontPolling();
    observer.observe(document.body, { childList: true, subtree: true });

})();