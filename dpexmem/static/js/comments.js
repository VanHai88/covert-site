!function(t){var n={};function o(r){if(n[r])return n[r].exports;var e=n[r]={i:r,l:!1,exports:{}};return t[r].call(e.exports,e,e.exports,o),e.l=!0,e.exports}o.m=t,o.c=n,o.d=function(t,n,r){o.o(t,n)||Object.defineProperty(t,n,{enumerable:!0,get:r})},o.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},o.t=function(t,n){if(1&n&&(t=o(t)),8&n)return t;if(4&n&&"object"==typeof t&&t&&t.__esModule)return t;var r=Object.create(null);if(o.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:t}),2&n&&"string"!=typeof t)for(var e in t)o.d(r,e,function(n){return t[n]}.bind(null,e));return r},o.n=function(t){var n=t&&t.__esModule?function(){return t.default}:function(){return t};return o.d(n,"a",n),n},o.o=function(t,n){return Object.prototype.hasOwnProperty.call(t,n)},o.p="/",o(o.s=0)}([function(t,n,o){t.exports=o(1)},function(t,n,o){"use strict";o.r(n);var r=".coral-count",e="coral-script";var c=function(){return void 0!==window.CoralCount};var a=function(){var t=document.querySelector('link[rel="canonical"]');return t?t.href:(console.warn("This page does not include a canonical link tag. Coral has inferred this story_url from the window object. Query params have been stripped, which may cause a single thread to be present across multiple pages."),(location.origin||"".concat(window.location.protocol,"//").concat(window.location.host))+window.location.pathname)};var u=function(t,n,o){var r=document.createElement("script");r.src="".concat(t,"?callback=").concat(n),Object.keys(o).forEach(function(t){var n="";void 0!==o[t]&&(n="string"==typeof o[t]?o[t]:JSON.stringify(o[t]),r.src+="&".concat(t,"=").concat(encodeURIComponent(n)))}),document.body.appendChild(r)};var i=function(t){var n,o,r=document.currentScript;if(!r&&t&&((r=document.getElementById(t))||(r=document.querySelector(".".concat(t)))),!r)throw new Error("Current script not found");return n=r.src,o=n.split("/"),"".concat(o[0],"//").concat(o[2])};var l=function(){window.CoralCount={setCount:function(t){var n=document.querySelectorAll("".concat(r,"[data-coral-ref='").concat(t.ref,"']"));Array.prototype.forEach.call(n,function(n){n.innerHTML=t.html})}}};function f(){var t=i(e),n=a(),o={},c=document.querySelectorAll(r);Array.prototype.forEach.call(c,function(t){var r=t.dataset.coralUrl,e=t.dataset.coralId,c="true"===t.dataset.coralNotext;r||e||(r=n,t.dataset.coralUrl=n);var a={id:e,url:r,notext:c},u=function(t){return btoa("".concat(JSON.stringify(!!t.notext),";").concat(t.id||t.url))}(a);u in o||(o[u]=a),t.dataset.coralRef=u}),Object.keys(o).forEach(function(n){var r=o[n],e={url:r.url,id:r.id,notext:r.notext?"true":"false",ref:n};u("".concat(t,"/api/story/count.js"),"CoralCount.setCount",e)})}function d(){l(),f()}o.d(n,"main",function(){return d}),c()||d()}]);
//# sourceMappingURL=count.js.map