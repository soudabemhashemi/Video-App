function applyLikeDislike(element) {

    const url = element.getAttribute("data-url")
    let data = {'type': element.getAttribute("data-type")}

    axios.post(
        url, data, {headers: {"X-CSRFToken": csrftoken}}
    ).then(
        (response) => {
            document.getElementById("like").innerHTML =  toPersian(response.data['like'].toString());
            document.getElementById("dislike").innerHTML =  toPersian(response.data['dislike'].toString());
            let text = '';
            if(response.data['is_increased']) {
                element.querySelector('i').classList.add("text-red");
                text = response.data.message;
            }
            else{
                element.querySelector('i').classList.remove("text-red");
                text = response.data.message;
            }
            if (data['type'] == 'like'){
                document.getElementById("dislike").classList.remove("text-red");
                text = response.data.message;
            }
            else{
                document.getElementById("like").classList.remove("text-red");
                text = response.data.message;
            }
            createToast(text);
        }
    ).catch(errors => window.location.href = serverData.urls.login + "?next=" + window.location.pathname)
};

function applyWatchLater(element){
    if(element.getAttribute("user") !== 'AnonymousUser') {
        const url = element.getAttribute("data-url")
        const videoCode = element.getAttribute("data-video")
        let data = {'video': videoCode}
        let headers = {"X-CSRFToken": csrftoken}
        if (element.getAttribute("is_added") === "True") {
            data['action'] = 'remove'
            axios.post(
                url, data, {headers: headers}
            ).then(
                (response) => {
                    element.querySelector('i').classList.remove("text-red");
                    element.setAttribute('is_added', 'False');
                    createToast(response.data.message);
                }
            ).catch(
                (response) => {
                    createToast("Something went wrong")
                }
            )
        } else {
            data['action'] = 'add'
            axios.post(
                url, data, {headers: headers}
            ).then(
                (response) => {
                    element.querySelector('i').classList.add("text-red");
                    element.setAttribute('is_added', 'True');
                    createToast(response.data.message);
                }
            ).catch(
                (response) => {
                    createToast("Something went wrong")
                }
            )
        }
    }
    else{
        window.location.href = serverData.urls.login + "?next=" + window.location.pathname
    }
}

$(document).ready(function() {

	let ellipsesText = "...";
	let moreText = "\nبیشتر";
	let lessText = "\nکمتر";
	$('.more-less').each(function() {
		let content = $(this).html();
        let charLimit;
        let lineLimit;
        if ($(this)[0].id === 'comment'){
            charLimit = 150;
            lineLimit = 2;
        }
        else if($(this)[0].id === 'description'){
            charLimit = 350;
            lineLimit = 5;
        }

        let lines = content.split('\n')

        let firstPart;
        let secondPart;
        let html;
        if(content.length > charLimit) {
			firstPart = content.substr(0, charLimit);
			secondPart = content.substr(charLimit-1, content.length - charLimit);

			html = firstPart + '<span class="moreellipses">' + ellipsesText+ '&nbsp;</span><span class="more-content"><span>' + secondPart + '</span>&nbsp;&nbsp;<a href="" class="more-link text-primary d-block" style="margin-top: -13px;">' + moreText + '</a></span>';

			$(this).html(html);
		}
        else if(lines.length > lineLimit) {
            firstPart = lines.slice(0, lineLimit).join('\n')
			secondPart = lines.slice(lineLimit, lines.length).join('\n')

			html = firstPart+'\n' + '<span class="more-content"><span>' + secondPart + '</span><a href="" class="more-link text-primary d-block" style="margin-top: -13px;">' + moreText + '</a></span>';

			$(this).html(html);

        }

	});

	$(".more-link").click(function(){
		if($(this).hasClass("کمتر")) {
			$(this).removeClass("کمتر");
			$(this).html(moreText);
		} else {
			$(this).addClass("کمتر");
			$(this).html(lessText);
		}
		$(this).parent().prev().toggle();
		$(this).prev().toggle();
		return false;
	});
});
