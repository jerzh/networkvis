// this script is nasty, no wonder people use jQuery

var md = window.markdownit();
var td = new TurndownService();

// add support for strikethrough (apparently Python Markdown doesn't support
// strikethrough so it won't work in the 'description' section but it's ok)
td.addRule('strikethrough', {
  filter: ['del', 's', 'strike'],
  replacement: function (content) {
    return '~~' + content + '~~';
  }
});

// choose black or white text color
var title = document.getElementById('title');
var c = getComputedStyle(title)['background-color'].match(/^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$/i);
title.style['color'] = (c[1] * 0.299 + c[2] * 0.587 + c[3] * 0.114) > 186 ? 'black' : 'white';

var description = document.getElementById('description');
c = getComputedStyle(description)['background-color'].match(/^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$/i);
if (c == null) {
  description.style['color'] = 'white';
} else {
  description.style['color'] = (c[1] * 0.299 + c[2] * 0.587 + c[3] * 0.114) > 186 ? 'black' : 'white';
}

var content = document.getElementById('content');
c = getComputedStyle(content)['background-color'].match(/^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$/i);
content.style['color'] = (c[1] * 0.299 + c[2] * 0.587 + c[3] * 0.114) > 186 ? 'black' : 'white';

// convert HTML to text on focus, convert back on unfocus
function tdf() {
  this.innerHTML = '<p>' + td.turndown(this.innerHTML) + '</p>';
}

function mdf() {
  this.innerHTML = md.render(this.innerText);
}

description.addEventListener('focusin', tdf);
description.addEventListener('focusout', mdf);
content.addEventListener('focusin', tdf);
content.addEventListener('focusout', mdf);

// save changes
document.getElementById('save').onclick = function() {
  document.getElementById('input-title')
    .setAttribute('value', document.getElementById('title').innerText);
  document.getElementById('input-desc')
    .setAttribute('value', td.turndown(document.getElementById('description').innerHTML));
  document.getElementById('input-content')
    .setAttribute('value', td.turndown(document.getElementById('content').innerHTML));
  document.getElementById('input-color')
    .setAttribute('value', document.getElementById('color').innerText);
  document.getElementById('input-desc-color')
    .setAttribute('value', document.getElementById('desc-color').innerText);
  document.getElementById('save-form').submit();
};

// revert changes (just reloads the page)
document.getElementById('revert').onclick = function() {
  window.location.reload();
};
