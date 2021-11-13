$(document).ready(function(){
   var url=document.location.href;
          $.each($("#category-na,e a"),function(){
    if(this.href==url){$(this).addClass('active');};
   });
});
