$(document).ready(function(){
var hidden_output = 1


$(document).off().on('click','.resulttree',function() {
    console.log('Click');
    var query = $(this).children('.output');
    var isVisible = query.is(':visible');
    if (isVisible === true) {
       query.hide();
    } else {
       query.show();
    }
});



$(document).on('click','.hideoutput',function() {
    console.log('Hide/show all');
    if (hidden_output == 0){
        console.log('Call hide');
        $('.resulttree').children('.output').hide() 
        hidden_output = 1
    }
    else  {
        console.log('Call show');
        $('.resulttree').children('.output').show()
        hidden_output = 0
    }
});

$('.resulttree').children('.output').hide();
})

