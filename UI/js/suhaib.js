
function addBox(id) {
	console.log("running Addbox");
	var $box = $(
"<div id='b" + id + "' class='box' style='width:290px;'>"
+"			<div class='static'>"
+"				<h2>Title</h2><img class='twittercue' src='twitter.png'>"
+"			</div>"
+"			<p class='summary'>Lorem ipsum itae interdum metus cursus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubili. Lorem ipsum itae interdum metus cursus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubili. Lorem ipsum itae interdum metus cursus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubili. Lorem ipsum itae interdum metus cursus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubili.Lorem ipsum itae interdum metus cursus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubili. Lorem ipsum itae interdum metus cursus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubili. Lorem ipsum itae interdum metus cursus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubili. Lorem ipsum itae interdum metus cursus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubili.</p>"
+"			<div class='ondemand'>"
+"				<img class='tempcloud' src='http://www.satyamnayak.com/wp-content/uploads/2009/02/relationships.png'/>"
+"				<p>Public Reaction: <b>Neutral</b></p>"
+"				<div class='scrollable'>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"					<p>Tweetstweetstweets</p>"
+"				</div>"
+"			</div>"
+"	</div>");


	$("#currentNews").append( $box ).masonry( 'appended', $box, true );
	$static = $('#b'+id+' .static');
	//Initialise display 
	$('#b'+id).data('display', 0);
	//hide ondemand part, match its height to summary
	$('#b'+id).children('.ondemand').hide().height($('#b'+id).children('.summary').height());
	//Define event actions
	$("#b"+id).click(
					function(){
						console.log("clicked!");
						console.log($(this));
						// if($(this).data('display')){
						// 	//remove it
						// 	$(this).children('.ondemand').hide()
						// 	$(this).children('.summary').show();
						// }else{
						// 	//show it
						// 	$(this).children('.summary').hide();
						// 	$(this).children('.ondemand').show();
						// }
						$(this).data('display', $(this).data('display') ? 0 : 1);
						$(this).css('background-color',	$(this).data('display') ? 'orange' : '#D8D5D2')
						
					}
				).hover(
						//handlerin
						function(){
							console.log("hoverin");
							if($(this).data('display') == 0){
								$(this).children('.summary').hide();
								$("#b"+id).children('.ondemand').show();
							}
						},
						//handlerout
						function(){
							console.log($(this).data('display'));
							if($(this).data('display') == 0){
								$(this).children('.ondemand').hide()
								$("#b"+id).children('.summary').show();
							}
						})
}

function changeBox(boxnum) {
	console.log("running changeBox");
	return function(data) {
		if (!document.getElementById("b" + boxnum)) { 
			addBox(boxnum);
			$('#currentNews').masonry('reload');
		}
		summary = data.short_summary;
		if(data.long_summary != null) summary = data.long_summary;
		$("#bt"+boxnum).html("<h2>" + data.title + "</h2><p>" + summary + "</p>");
	}
}

function boxClick() {
	
}

$(document).ready(function() {
	console.log("ready");
	$('#currentNews').masonry({
		// options
		itemSelector : '.box',
		isAnimated: true,
		isFitWidth: false,
		isResizable: true,
		columnWidth: 313,
	});

	$.getJSON("proxy.php?url=api/1/news", function(data) {
		console.log(data);
		for(i = 0; i < data.news.length; i++) {
			$.getJSON("proxy.php?url=api/1/story/"+data.news[i]+"/short", changeBox(i));
		}
	});
	//Testing
	addBox(1);
	addBox(2);
	addBox(3);
	addBox(4);
	addBox(5);
	addBox(6);
	
	//endTesting
});
