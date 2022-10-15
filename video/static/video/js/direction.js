   function checkRtl( character ) {
    var RTL = ['ا','ب','پ','ت','س','ج','چ','ح','خ','د','ذ','ر','ز','ژ','س','ش','ص','ض','ط','ظ','ع','غ','ف','ق','ک','گ','ل','م','ن','و','ه','ی'];
    return RTL.indexOf( character ) > -1;
};

var divs = document.getElementsByClassName('auto-direction')
for ( var index = 0; index < divs.length; index++ ) {
    if( checkRtl( divs[index].innerText.charAt(1) ) ) {
        divs[index].classList.add('rtl');
    } else {
        divs[index].classList.add('ltr');
    };
};


function direction(text){
    if( checkRtl( text.charAt(1) ) ) {
        return 'rtl'
    } else {
        return 'ltr'
    };
}
