$(document).ready(function () {

  // @rodluger: Create code version dropdown
  if (typeof (String.prototype.trim) === 'undefined') {
    String.prototype.trim = function () {
      return String(this).replace(/^\s+|\s+$/g, '');
    };
  }
  version_div = document.getElementsByClassName('version')[0];
  var current_version = version_div.innerHTML.trim();
  if (current_version != "latest") current_version = 'v' + current_version;
  version_div.innerHTML = '';
  version_selector = document.createElement('select');

  // @rodluger: Read code versions from github and add to dropdown
  var txtFile = new XMLHttpRequest();
  txtFile.open(
    'GET',
    'https://raw.githubusercontent.com/rodluger/rodluger.github.io/master/legacy/starry/versions.txt',
    true);
  txtFile.onreadystatechange = function () {
    if (txtFile.readyState === 4) {  // document is ready to parse.
      if (txtFile.status === 200) {  // file is found
        allText = txtFile.responseText;
        versions = txtFile.responseText.split('\n');
        for (var i in versions) {
          if (versions[i].length) {
            var op = new Option();
            op.value = versions[i];
            if (versions[i].trim() == current_version)
              op.selected = true;
            else
              op.selected = false;
            op.text = versions[i];
            version_selector.options.add(op);
            version_div.appendChild(version_selector);
          }
        }
      }
    }
  };
  txtFile.send(null);

  // @rodluger: Re-direct to the selected version's docs
  version_selector.onchange = function () {
    window.location.href = '/starry/' + this.value;
  }
})
