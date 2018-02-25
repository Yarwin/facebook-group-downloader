function makeGetRequest(theUrl, onComplete, onError) {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (request.readyState == 4 && request.status == 200) {
            onComplete(request.response);

        } else {
            onError(request.response);
        }
    };

    request.open("GET", theUrl, true);
    request.send();
}


function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    let regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}


function parse_results(results, accessToken) {
    document.getElementById("result").innerHTML = "Successfully authorised!";
    document.getElementById("group-header").innerHTML = `<h1>Your groups</h2>`;
    results["data"].map((res) => {
        let groupHtml = `
        <div class="group-name">${res.name}</div>
        <div class="button">
            <form method='POST' action='/get-group/'>
                <input type='hidden' value='${res.id}' name='group_id'>
                <input type='hidden' value='${res.name}' name='group_name'>
                <input type='hidden' value='${accessToken}' name='user_token'>
                <input class="btn" type="submit" name='Scrap group' value="Scrap group!">
            </form>
        </div>`;
        document.getElementById("groups").innerHTML += groupHtml;
    })
}

function handleError(result) {
    document.getElementById("result").innerHTML = `Error - ${result.error.message}!`;
}

function main() {
    let accessToken = getParameterByName('#access_token');
    let fbUrl = "http://graph.facebook.com/me/groups?access_token=" + accessToken;
    makeGetRequest(fbUrl, (results) => parse_results(JSON.parse(results), accessToken),
        (result) => handleError(JSON.parse(result))
    );
}

window.onload = main();