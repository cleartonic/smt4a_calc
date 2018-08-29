// https://api.twitch.tv/kraken/channels/cleartonic/subscriptions?oauth_token=1kmxs5mz8mljque9h0rrc9z5u3or87
// Sub page example
// ?oauth_token=1kmxs5mz8mljque9h0rrc9z5u3or87
// Channel ID: 46167428
// pass1 = Last Sub
// pass2 = Last Follower




// To do: Consider long term having css background update when notifications happen. 

/* Declarations */
var activesubqueue = 0
var notifyqueue = []



/* Settings */
var widthsetting = 1 // 1: 'snes' , 2: 'gba'
var playsounds = 1
var slotson = 0
var challengeon =  1
var challengeamount = 5

/* File Lookup */
var newsubnoise = new Audio('notificationsounds/S3K_B8.wav')
var subnoise = new Audio('notificationsounds/S3K_63.wav')
var bitnoise = new Audio('notificationsounds/S3K_B0.wav')
//var bitnoise = new Audio('notificationsounds/kelv.wav')
var hostnoise = new Audio('notificationsounds/S3K_AA.wav')




$(document).ready(function(){
pubsubconnect();     // PubSub Connect
queuenotify(); // start notification queue
widthcheck(widthsetting); //set width either SNES or GBA
soundcheck(playsounds); //displays alertsoff image if playsounds = 0
challengecheck(challengeon, widthsetting); // Disable html divs if challenge is off
//testloop(); 
//testnotify2()
});



/* Width settings */
function widthcheck(widthsetting) {
	switch(widthsetting) {
		case 1:
			$("#notificationwrapper").css("width",316)
			break;
		case 2:
			$("#notificationwrapper").css("width",236)
			break;
	}
}

/*   Alerts Code   */

function notificationupdate(notificationname, notificationmonths, notificationbits, notificationtotalbits, notificationmessage, notificationtype) {

	playsound(notificationtype)
    switch (notificationtype) { // swap between sub, bits and donations
	
	
        case "newsub": // sub notification
            console.log("New Sub Alert")
			// $('#metalslime').show();
			$('#metalslime').addClass("animated fadeIn");
            var notificationnamestring1 = notificationname.fontcolor("00ff00").bold().big()
            var notificationmonthanimationtype = "fadeInDown";
            $('#notificationName').append(notificationnamestring1);
            $('#notifyLogo').show();
			$('#notifyLogoImage').attr('src', 'notificationimg/ct.png');
            $('#notifyLogoImage').show();
			
            $('#notifyLogo').addClass("animated rotateIn")
            $('#notifyLogo').one('webkitAnimationEnd', function() {
                $('#notifyText').show();
                $('#notifyText').append("NEW Sub!");
                $('#notifyText').addClass("animated fadeInLeft")
            })
            $('#notifyText').one('webkitAnimationEnd', function() {
                $('#notificationName').show();
                $('#notificationName').addClass("animated bounceInLeft");
                $('#clearFacial').show();
                $('#clearFacial').addClass("animated fadeInDown");
            });
            setTimeout(function() {
                resetnotify()
            }, 10000); // NOTE : either need to pass arguments specific to each notificationtype, or make 1 big generic one
			break;
	
	
	
	
	
        case "resub": // sub notification
            console.log("Resub Alert")
			// $('#metalslime').show();
			$('#metalslime').addClass("animated fadeIn");			
            var notificationnamestring1 = notificationname.fontcolor("0fffff").bold().big()
            var notificationmonthanimationtype = "fadeInDown";
            $('#notificationName').append(notificationnamestring1);
            $('#notifyLogo').show();
			$('#notifyLogoImage').attr('src', 'notificationimg/ct.png');
            $('#notifyLogoImage').show();
			
            $('#notifyLogo').addClass("animated rotateIn")
            $('#notifyLogo').one('webkitAnimationEnd', function() {
                $('#notifyText').show();
                $('#notifyText').append("sub life with ");
                $('#notifyText').addClass("animated fadeInLeft")
            })
            $('#notifyText').one('webkitAnimationEnd', function() {
                $('#notificationName').show();
                $('#notificationName').addClass("animated bounceInLeft");
                setTimeout(function() {
                        $('#notificationMonths').append(notificationmonths);
                        $('#notificationMonths').show();
                        $('#notificationMonths').addClass("animated " + notificationmonthanimationtype);
                    }, 2000) // notificationmonth alert time
                setTimeout(function() {
                        $('#notificationMonthstext').show();
                        $('#notificationMonthstext').addClass("animated fadeIn");
                    }, 3000) // notificationmonth alert time
            });
            setTimeout(function() {
                resetnotify()
            }, 10000); // NOTE : either need to pass arguments specific to each notificationtype, or make 1 big generic one
			break;
			
			
			
			
			
        case "bit": // bit notification
			// $('#metalslime').show();
			$('#metalslime').addClass("animated fadeIn");
            console.log("Bit Alert")
			if (notificationbits >= 5) {
				slotsStart()
				};
			if (notificationbits >= challengeamount) {
				if (challengeon == 1) {
					challenge(notificationname,notificationmessage);
					};
				};	
			if (notificationbits >= 1000) {
					bitdonate1(notificationbits);
				};
			var bitcolor = ""
			if (notificationbits >= 100000) { bitcolor = "ffff66" } 
				else if (notificationbits >= 10000 ) {bitcolor = "ff6666"} 
				else if (notificationbits >= 5000) {bitcolor = "4d94ff"} 
				else if (notificationbits >= 1000) {bitcolor = "66ffd9"} 
				else if (notificationbits >= 100) {bitcolor = "8c66ff"} 
				else {bitcolor = "808080"} ;	
				
            var notificationnamestring1 = notificationname.fontcolor(bitcolor).bold().big()
            var notificationmonthanimationtype = "fadeInDown";
            $('#notificationName').append(notificationnamestring1);
			var biticon = ""
			if (notificationbits >= 100000) { biticon = "notificationimg/bit-gold.gif" } 
				else if (notificationbits >= 10000 ) {biticon = "notificationimg/bit-red.gif"} 
				else if (notificationbits >= 5000) {biticon = "notificationimg/bit-blue.gif"} 
				else if (notificationbits >= 1000) {biticon = "notificationimg/bit-green.gif"} 
				else if (notificationbits >= 100) {biticon = "notificationimg/bit-purple.gif"} 				
				else {biticon = "notificationimg/bit-grey.gif"};					
            $('#notifyLogoImage').attr('src', biticon);
            $('#notifyLogo').addClass("animated fadeInDown")
            $('#notifyLogo').show();
            $('#notifyLogoImage').show();
            $('#notifyLogo').one('webkitAnimationEnd', function() {
                $('#notifyText').show();
                $('#notifyText').append("   " + notificationbits + " bits from "+ notificationnamestring1);
                $('#notifyText').addClass("animated fadeInLeft")
            });
            setTimeout(function() { // 1) delay donated bits + # fadeOut
                $('#notifyText2').show();
                $('#notifyText2').append(notificationmessage);
                $('#notifyText2').attr('class', 'scroll1')
                $('#notifyText2').addClass("animated fadeInLeft");
                $('#notifyLogo').removeClass();
                $('#notifyText').removeClass();
                $('#notifyLogo').addClass("animated fadeOutUp");
                $('#notifyText').addClass("animated fadeOutUp");
                setTimeout(function() { // 2) animate total bits
                    $('#notifyLogo').hide();
                    $('#notifyLogoImage').hide();
                    $('#notifyLogo').removeClass();
                    $('#notifyText').removeClass();

					var bitbadge = ""
					if (notificationtotalbits >= 100000) { bitbadge = "notificationimg/badge-gold.png" } 
						else if (notificationtotalbits >= 10000 ) {bitbadge = "notificationimg/badge-red.png"} 
						else if (notificationtotalbits >= 5000) {bitbadge = "notificationimg/badge-blue.png"} 
						else if (notificationtotalbits >= 1000) {bitbadge = "notificationimg/badge-green.png"} 
						else if (notificationtotalbits >= 1000) {bitbadge = "notificationimg/badge-purple.png"} 				
						else {bitbadge = "notificationimg/badge-grey.png"};						
                    $('#notifyLogoImage').attr('src', bitbadge);
                    $('#notifyText').empty();
                    $('#notifyText').append("   " + notificationtotalbits);
                    $('#notifyLogo').show();
                    $('#notifyLogoImage').show();
                    $('#notifyLogo').addClass("animated fadeInDown");
                    $('#notifyText').addClass("animated fadeInDown");
                }, 1000); // 2) animate total bits
            }, 5000); // 1) delay donated bits + # fadeOut
            setTimeout(function() {
                resetnotify()
            }, 10000); // NOTE : either need to pass arguments specific to each notificationtype, or make 1 big generic one
            break;
			
			
			
			
			
        case "host": // host notification (THIS USES THE MONTH PARAMETER FOR # OF VIEWERS)
			//$('#metalslime').show();
			$('#metalslime').addClass("animated fadeIn");		
            console.log("New Host")
            var notificationnamestring1 = notificationname.fontcolor("ff66ff").bold().big();
			var notificationmonthstring1 = String(notificationmonths)
            var notificationmonthstring2 = notificationmonthstring1.fontcolor("66d9ff").bold().big();
            $('#notifyLogo').show();
			$('#notifyLogoImage').attr('src', 'notificationimg/ct.png');
            $('#notifyLogoImage').show();
			
            $('#notifyLogo').addClass("animated rotateIn")
            $('#notifyLogo').one('webkitAnimationEnd', function() {
                $('#notifyText').show();
                $('#notifyText').append("New host from " + notificationnamestring1 + " for " + notificationmonthstring2 + " viewers");
                $('#notifyText').addClass("animated fadeInLeft")
            })
            $('#notifyText').one('webkitAnimationEnd', function() {
                $('#clearRoll').show();
                $('#clearRoll').addClass("animated fadeInDown");
								
				
            });
            setTimeout(function() {
                resetnotify()
            }, 10000); // NOTE : either need to pass arguments specific to each notificationtype, or make 1 big generic one
            break;

    }

}




function slotsStart() {
	if (slotson == 1) {
	$(".machine").show();
	$(".machine").addClass("animated flipInX");
	setTimeout( function () { widget.beforeRun() } , 2000);
	setTimeout( function () { 
	
/* 		$(".machine").removeClass("animated");
			$(".machine").hide();  */
			
		$(".machine").removeClass("animated flipInX");
		$(".machine").addClass("animated flipOutX");		
 		$('.machine').one('webkitAnimationEnd', function() {
			$(".machine").removeClass("animated flipOutX");
			$(".machine").hide(); 
			}); 
			
	}, 11000);
	}
}



function playsound(notificationtype) {
	if (playsounds == 1) {
		switch (notificationtype) {
			case "newsub":
				newsubnoise.load();
				newsubnoise.play();
				break;
			case "resub":
				subnoise.load();
				subnoise.play();
				break;
			case "bit":
				bitnoise.load();
				bitnoise.play();
				break;
			case "host":
				break;
		};
	};
	if (playsounds == 0) {
		$("#alertsoffimage").show()
		}
}

function soundcheck(playsounds) {
	if (playsounds == 0) {
		$("#alertsoffimage").show()
		}
}


/* QUEUE FOR NOTIFICATIONS  */



	
function pushqueue (a,b,c,d,e,f) {  // arguments are for notificationupdate
	var queuepush = {notificationname:a, notificationmonths:b, notificationbits:c, notificationtotalbits:d, notificationmessage:e, notificationtype:f};
	notifyqueue.push(queuepush);

}

function queuenotify() {
    if (activesubqueue == 0) {
        activesubqueue = 1
        if (notifyqueue.length > 0) {
            notificationupdate(notifyqueue[0].notificationname, notifyqueue[0].notificationmonths, notifyqueue[0].notificationbits, notifyqueue[0].notificationtotalbits, notifyqueue[0].notificationmessage, notifyqueue[0].notificationtype);
			notifyqueue.shift()
            activesubqueue = 0;
			setTimeout(function () { queuenotify() }, 15000);
        } else { ;
            activesubqueue = 0;
            console.log("Queue is empty");
            setTimeout(function () { queuenotify() }, 15000);
        };
    } else {
      console.log("activesubqueue: " + activesubqueue);      
      setTimeout(function () { queuenotify() }, 15000);
    };
}

	

function resetnotify() {

	
    $('#notifyLogo').removeClass();
    $('#notifyText').removeClass();
    $('#notifyText2').removeClass();
	$('#notificationName').removeClass();
    $('#notificationMonths').removeClass();
    $('#notificationMonthstext').removeClass();
    $('#clearFacial').removeClass();	
	$('#clearRoll').removeClass();	
    setTimeout(function() {
        $('#notifyLogo').addClass("animated fadeOutUp");
        $('#notificationName').addClass("animated fadeOutUp");
        $('#notifyText').addClass("animated fadeOutUp");
        $('#notifyText2').addClass("animated fadeOutUp");
        $('#notificationMonths').addClass("animated fadeOutUp");
        $('#notificationMonthstext').addClass("animated fadeOutUp");
		$('#clearFacial').addClass("animated fadeOutUp");
		$('#clearRoll').addClass("animated fadeOutUp");	
		$('#metalslime').addClass("animated fadeOut");	
		
    }, 2000)
    setTimeout(function() {
        $('#notifyLogo').hide();
        $('#notificationName').hide();
        $('#notifyText').hide();
        $('#notifyText2').hide();
        $('#notificationMonths').hide();
        $('#notificationMonthstext').hide();
        $('#clearFacial').hide();	
		$('#clearRoll').hide();			
        
		$('#notifyLogo').removeClass();
        $('#notificationName').removeClass();
        $('#notifyText').removeClass();
        $('#notifyText2').removeClass();
        $('#notificationMonths').removeClass();
        $('#notificationMonthstext').removeClass();
        $('#clearFacial').removeClass();	
		$('#clearRoll').removeClass();	
			
		$('#notifyText').empty();
        $('#notifyText2').empty();
        $('#notificationName').empty();
        $('#notificationMonths').empty();

		$('#metalslime').removeClass();
		$('#metalslime').hide();		
    }, 3000)
}






// INFORMATION LOOP



var animationpool = ["bounceInLeft", "bounceInLeft", "fadeInRight", "fadeInUp", "fadeInDown", "fadeInLeft"]
var textanimations = ["cleartonic",10000,"@cleartonic",5000,"discord.gg/cleartonic", 5000,"!commands",5000]
var logoanimations = ['http://i.imgur.com/FrdjwsD.png',10000,'http://i.imgur.com/tD2pTg4.png',5000,'http://i.imgur.com/k98wbWB.png',5000,'http://i.imgur.com/FrdjwsD.png',5000]


$(document).ready(function(){
infoTextLoop();
infoLogoLoop();
});

function infoTextLoop() {
		var randomanimation = animationpool[Math.floor(Math.random()*animationpool.length)];
		var texttext = textanimations[0]
		var textlength = textanimations[1]
		textanimations.shift();
		textanimations.shift();
		textanimations.push(texttext);
		textanimations.push(textlength);
			$('#infoText').empty();
			$('#infoText').append(texttext);		// VAR 1
			$('#infoText').addClass("animated " + randomanimation);		
			$('#infoText').show();
			setTimeout( function () { 
				$('#infoText').removeClass();
				$('#infoText').addClass("animated fadeOutLeft");		
				setTimeout( function() {
					$('#infoText').hide();
					$('#infoText').removeClass();
					setTimeout ( infoTextLoop, 1000);
			},2000);
			}, textlength);
}

function infoLogoLoop() {
		var randomanimation = animationpool[Math.floor(Math.random()*animationpool.length)];
		var logologo = logoanimations[0]
		var logolength = logoanimations[1]
		logoanimations.shift();
		logoanimations.shift();
		logoanimations.push(logologo);
		logoanimations.push(logolength);
			$('#infoLogoImage').attr('src', logologo);
			$('#infoLogo').addClass("animated " + randomanimation);		
			$('#infoLogo').show();
			setTimeout( function () { 
				$('#infoLogo').removeClass();
				$('#infoLogo').addClass("animated fadeOutLeft");		
				setTimeout( function() {  //webkitanimation2			
					$('#infoLogo').hide();
					$('#infoLogo').removeClass();
					setTimeout ( infoLogoLoop, 1000);
			},2000);
			}, logolength);
}



// Notification procs

function bitdonate1(notificationbits) {
	$('#infoBitdonateImage').show();
	setTimeout ( function () {$('#infoBitdonateImage').hide(); }, 10000);	
	
	
}






/* Test functions */

function testloop () {
	pushqueue("tonikku",0,99119,4148,"magman man","bit");	
	setTimeout ( function () { testloop () }, 5000)
}
function testnotify1 ()  {
	pushqueue("tonikku",1,0,0," ","newsub"); 
	}

function testnotify2 ()  {
	pushqueue("tonikku",0,1,4148,"jewel man metal man","bit");
	pushqueue("tonic",0,11,438,"nitro man","bit");
	pushqueue("tonikka",0,111,4148,"jewel man","bit");
	pushqueue("tonikko",0,2111,3348,"nitro man","bit");
	pushqueue("tonikke",0,33319,418,"jewel man","bit");
}


function testnotify3 ()  {
	// notificationupdate("tonikku",1,0,0,"","newsub"); // trying out queue below
	pushqueue("TONIC-SAN",119,0,0," ","resub"); 
	}
	
function testnotify4 ()  {
	// notificationupdate("tonikku",1,0,0,"","newsub"); // trying out queue below
	pushqueue("Liquid Metal",66,0,0," ","host"); 
	}	

