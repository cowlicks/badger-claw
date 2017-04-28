function getIndex() {
  xhr = new XMLHttpRequest();
  xhr.open("GET", "/results/index.json", true);
  xhr.setRequestHeader("Content-type", "application/json");
  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4 && xhr.status == 200) {
      var json = JSON.parse(xhr.responseText);
      var resultEl = document.getElementById("results-list");
      resultEl.innerHTML = parseIndex(json);
    }
  }
  xhr.send();
}

function getCommit(suffix) {
  return suffix.split('-')[1].split('.')[0];
}

function getDate(suffix) {
  return suffix.split('-')[0].split('_');
}


function parseSuffix(suffix) {
  var commit = getCommit(suffix).slice(0, 7);
  var date = getDate(suffix);
  var out = "";
  out += "<a href=\"results/analysis-" + suffix + "\"> Analysis </a>";
  out += " and <a href=\"results/data-" + suffix + "\"> data </a><br>";
  out += "Commit <code> " + commit + "</code> on date ";
  out += "" + date[0] + "-" + date[1] + "-" + date[2] + " ";
  out += "at " + date[3] + ":" + date[4] + " " + date[5].toLowerCase();
  return out;
}


function parseIndex(results) {
  var numResultsToShow = 10;
  var index = results["index"];
  var out = "<ul>";
  var rlen = index.length;
  if (rlen > numResultsToShow) {
    rlen = numResultsToShow;
  }

  for (var i = 0; i < rlen; i++) {
      var s = index[i];
      out += "<li>" + parseSuffix(s) + "</li>";
  }
  out += "</ul>";
  return out;
}

getIndex();
