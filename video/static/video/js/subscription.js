function subscribe(event, other) {
    let data = {}
    axios.post(event.getAttribute("path"), data, {headers: {"X-CSRFToken": csrftoken}}
    ).then(
        response => {
            event.classList.remove("d-flex");
            event.classList.add("d-none");

            document.getElementById(other).classList.remove("d-none");
            // document.getElementById('unsubscribe').classList.add("d-flex");

            if(document.getElementById('number-of-subscribers') && other == 'unsubscribe-this')
                document.getElementById('number-of-subscribers').innerHTML = toPersian(response.data['subscribers'].toString());
            createToast('Subscription added');
        }
    ).catch(function (error) {
        if (error.response.status == 403) {
          window.location.href = serverData.urls.login + "?next=" + window.location.pathname
        }
    })
}

function unsubscribe(event, other) {
    let data = {}
    axios.post(event.getAttribute("path"), data, {headers: {"X-CSRFToken": csrftoken}}
    ).then(
        response => {
            event.classList.remove("d-flex");
            event.classList.add("d-none");

            document.getElementById(other).classList.remove("d-none");
            // document.getElementById('subscribe').classList.add("d-flex");

            if(document.getElementById('number-of-subscribers') && other == 'subscribe-this')
                document.getElementById('number-of-subscribers').innerHTML = toPersian(response.data['subscribers'].toString());
            createToast('Subscription removed');
        }
    ).catch(function (error) {
        if (error.response.status == 403) {
          window.location.href = serverData.urls.login + "?next=" + window.location.pathname
        }
    })
}