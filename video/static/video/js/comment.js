function createComment(data) {
    let newComment = document.createElement("div");
    dir = direction(data["text"])
    if (data["channel"].avatar) {
        newComment.innerHTML =
            '<div class="mt-2 pe-1">' +
                '<div class="row pb-2">' +
                    '<div class="col-12 col-md-6 d-flex flex-row bd-highlight">' +
                        '<a class="row default-avatar">' +
                            '<img class="rounded-circle user-img px-0" style="width: 50px !important; height: 50px !important; object-fit: cover;" src="' + data["channel"].avatar + '" alt="avatar" width="50" height="50">'+
                            '<p class="col m-t-30 text-end" id="name" style="margin-right: .1rem!important;">' + data["channel"].title + '</p>' +
                        '</a>' +
                        '<small class="m-t-30 ms-3 fs-10 text-muted">' + data["sent_at"] + '</small>' +
                    '</div>' +
                    '<pre class="text-end px-1-9 ms-5 w-90 overflow-hidden ' + dir + ' " style="margin-top: -21px;">' + data["text"] + '</pre>' +
                '</div>' +
            '</div>'
        ;
    }
    else{
        newComment.innerHTML =
            '<div class="mt-2 pe-1">' +
                '<div class="row pb-2">' +
                    '<div class="col-12 col-md-6 d-flex flex-row bd-highlight">' +
                        '<a class="row default-avatar">' +
                            '<div id="profileImage" class="rounded-circle user-img px-0 fs-5" style="padding-top: .73rem; width: 50px; height: 50px;" >' + data["channel"].name[0] +'</div>' +
                            '<p class="col m-t-30 text-end" id="name" style="margin-right: .1rem!important;">' + data["channel"].title + '</p>' +
                        '</a>' +
                        '<small class="m-t-30 ms-3 fs-10 text-muted">' + data["sent_at"] + '</small>' +
                    '</div>' +
                    '<pre class="text-end px-1-9 ms-5 w-90 overflow-hidden ' + dir + ' " style="margin-top: -21px;">' + data["text"] + '</pre>' +
                '</div>' +
            '</div>'
        ;

    }
    return newComment;
}


let commentButton = document.getElementById('commentButton');
if (commentButton) {
    commentButton.addEventListener('click', function (event) {
        event.preventDefault()
        let data = {}
        data['text'] = document.getElementById('comment-context').value
        axios.post(commentButton.getAttribute('data-url'), data, {headers: {"X-CSRFToken": csrftoken}}
        ).then(
            response => {
                cancel()
                document.getElementById("comments").prepend(createComment(response['data']))
                createToast('Your comment submitted')
            }
        ).catch(console.error())
    })
}

function openButton(){
    let commentButton = document.getElementById('commentButton');
    commentButton.classList.remove('d-none')
    commentButton.classList.add('d-flex')

    let cancelButton = document.getElementById('cancelButton');
    cancelButton.classList.remove('d-none')
    cancelButton.classList.add('d-flex')
}

function cancel(){
    document.getElementById("comment-context").value = ""
    let commentButton = document.getElementById('commentButton');
    commentButton.classList.remove('d-flex')
    commentButton.classList.add('d-none')

    let cancelButton = document.getElementById('cancelButton');
    cancelButton.classList.remove('d-flex')
    cancelButton.classList.add('d-none')

    document.getElementById('comment-context').style.height = 'auto';
}


$('textarea').on('input', function () {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
  let commentButton = document.getElementById('commentButton');
  commentButton.classList.add('btn-blue')
});