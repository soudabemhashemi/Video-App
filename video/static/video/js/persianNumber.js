let persian = {0: '۰', 1: '۱', 2: '۲', 3: '۳', 4: '۴', 5: '۵', 6: '۶', 7: '۷', 8: '۸', 9: '۹'};
$(document).ready(function(){
	function traverse(element){
		let i;
        if(element.nodeType==3){
            const list = element.data.match(/[0-9]/g);
            if(list!=null && list.length!=0){
				for(i = 0; i<list.length; i++)
					element.data=element.data.replace(list[i],persian[list[i]]);
			}
		}
		for(i = 0; i<element.childNodes.length; i++){
			traverse(element.childNodes[i]);
		}
	}
    traverse(document.body);
});

toPersian = function (str)
{
  if(typeof str === 'string')
  {
    for(var i=0; i<10; i++)
    {
      str = str.replace(i, persian[i])
    }
  }
  return str;
};