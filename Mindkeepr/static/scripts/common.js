$(document).ready(function () {

    var url = document.location.toString();
    if (url.match('#')) {
        $('.nav-tabs a[href="#' + url.split('#')[1] + '"]').tab('show');
    }

    // Change hash for page-reload
    $('.nav-tabs a').on('shown.bs.tab', function (e) {
        window.location.hash = e.target.hash;
    });

});

function convertISO8601ToHuman(date) {
    parsedDate = new Date(date);
    dateTimeFormat = new Intl.DateTimeFormat('en', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: "numeric",
        minute: "numeric"
      });
    return dateTimeFormat.format(parsedDate);
}

function convertISO8601ToHumanDay(date) {
    parsedDate = new Date(date);
    /*dateTimeFormat = new Intl.DateTimeFormat('en', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
     });
    return dateTimeFormat.format(parsedDate);*/
    dateTimeFormat = new Intl.DateTimeFormat('fr', {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
     });
    return dateTimeFormat.format(parsedDate);
}

function findGetParameter(parameterName) {
    var result = null,
        tmp = [];
    location.search
        .substr(1)
        .split("&")
        .forEach(function (item) {
          tmp = item.split("=");
          if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}