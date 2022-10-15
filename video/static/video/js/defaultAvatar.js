
    $(document).ready(function(){
        const containers = document.getElementsByClassName('default-avatar')
        let element;
        for (element of containers){
            if(element.querySelector('#profileImage')) {
                const name = element.querySelector('#name').innerText
                let intials = '$'
                for (let i in name){
                    if(name.charAt(i) !== ' ') {
                        intials = name.charAt(i)
                        break
                    }
                }
                element.querySelector('#profileImage').innerHTML = intials
            }
        }
    });
