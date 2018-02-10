/**
 * get url params
 * @param sParam
 * @returns {boolean}
 */
var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

var data = {"stream_secret":getUrlParameter('stream_secret')}
$(document).ready(function () {
});

$("button").click(function (e) {
    var name = e.target.name;
    console.log();
    if (name == "decrease-res") {
        data['name'] = name;
        data['value'] = name;
    } else if (name == "increase-res") {
        data['name'] = name;
        data['value'] = name;
    } else if (name == "reset-min-max") {
        data['name'] = name;
        data['value'] = name;
    } else if (name == "motion-detection") {
        data['name'] = name;
        data['value'] = name;
    }

    console.log(data)
    $.ajax({
        type: "POST",
        url: "/load_ajax",
        data: data,
        success: function (result) {
            console.log(result);
        }
    });
});

