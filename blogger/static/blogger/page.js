// this script is nasty, no wonder people use jQuery
/* right now I'm converting to Markdown on focus and converting back on unfocus,
which is suboptimal - ideally I want to save the unformatted text somewhere */
// no more Turndown - now the unformatted text is saved in variables

var md = window.markdownit();
// var td = new TurndownService();

// add support for strikethrough (apparently Python Markdown doesn't support
// strikethrough so it won't work in the 'description' section but it's ok)
// not using Turndown anymore so that is that

// td.addRule('strikethrough', {
//   filter: ['del', 's', 'strike'],
//   replacement: function (content) {
//     return '~~' + content + '~~';
//   }
// });

// set innerHTML for description and content + choose black or white text color
var title = document.getElementById('title-container');
var c = getComputedStyle(title)['background-color'].match(/^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$/i);
title.style['color'] = (c[1] * 0.299 + c[2] * 0.587 + c[3] * 0.114) > 186 ? 'black' : 'white';

var description = document.getElementById('description');
description.innerHTML = md.render(desc_text);
c = getComputedStyle(description)['background-color'].match(/^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$/i);
if (c == null) {
  description.style['color'] = 'white';
} else {
  description.style['color'] = (c[1] * 0.299 + c[2] * 0.587 + c[3] * 0.114) > 186 ? 'black' : 'white';
}

var content = document.getElementById('content');
content.innerHTML = md.render(content_text);
c = getComputedStyle(content)['background-color'].match(/^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$/i);
content.style['color'] = (c[1] * 0.299 + c[2] * 0.587 + c[3] * 0.114) > 186 ? 'black' : 'white';

var links = document.getElementsByClassName('link');
for (var i = 0; i < links.length; i++) {
  var link = links[i];
  c = getComputedStyle(link)['background-color'].match(/^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$/i);
  link.style['color'] = (c[1] * 0.299 + c[2] * 0.587 + c[3] * 0.114) > 186 ? 'black' : 'white';
}

// convert HTML to text on focus, convert back on unfocus
// had to make separate functions for each listener because the variables have
// different names rip

// function to_text() {
//   this.innerHTML = '<p>' + td.turndown(this.innerHTML) + '</p>';
// }
//
// function to_md() {
//   this.innerHTML = md.render(this.innerText);
// }

description.addEventListener('focusin', function() {
  this.innerHTML = '<p>' + desc_text + '</p>';
});
description.addEventListener('focusout', function() {
  desc_text = this.innerText;
  this.innerHTML = md.render(desc_text);
});
content.addEventListener('focusin', function() {
  this.innerHTML = '<p>' + content_text + '</p>';
});
content.addEventListener('focusout', function() {
  content_text = this.innerText;
  this.innerHTML = md.render(content_text);
});

if (editable) {
  // save changes
  document.getElementById('save').onclick = function() {
    document.getElementById('input-title')
      .setAttribute('value', document.getElementById('title').innerText);
    document.getElementById('input-desc')
      .setAttribute('value', desc_text);
    document.getElementById('input-content')
      .setAttribute('value', content_text);
    document.getElementById('input-color')
      .setAttribute('value', document.getElementById('color').innerText);
    document.getElementById('input-desc-color')
      .setAttribute('value', document.getElementById('desc-color').innerText);

    if (addable) {
      document.getElementById('input-author')
        .setAttribute('value', document.getElementById('add').innerText);
    }

    document.getElementById('save-form').submit();
  };

  // revert changes (just reloads the page)
  document.getElementById('revert').onclick = function() {
    window.location.reload();
  };

  // clear text when + button is clicked (decided against it because it causes
  // a bug if the user clicks 'save changes' without clicking out)
  // apparently it doesn't happen anymore? idk what happened
  var add = document.getElementById('add');
  if (add) {
    add.addEventListener('focusin', function () {
      add.innerText = '';
    });
  }
} else {
  // when not editable, make it obvious that buttons aren't clickable by changing
  // the cursor to default
  document.getElementById('title').style['cursor'] = 'default';
  document.getElementById('color').style['cursor'] = 'default';
  document.getElementById('desc-color').style['cursor'] = 'default';
  document.getElementById('save').style['cursor'] = 'default';
  document.getElementById('revert').style['cursor'] = 'default';
}
