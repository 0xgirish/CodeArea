$(document).ready(function(){
    	function updateLike(btn, newCount, verb){
    		btn.parent().children(".count").text(newCount);
    		if(verb){
    			btn.removeClass("btn-unlike");
    			btn.addClass("btn-rose");
    		}
    		else{
    			btn.removeClass("btn-rose");
    			btn.addClass("btn-unlike")
    		}
    	}
		$(".like-btn").click(function(e){
			e.preventDefault();
			var this_ = $(this);
			var likeUrl = this_.attr("data-href");
			console.log(likeUrl)
			$.ajax({
				url: likeUrl,
				method: "GET",
				data: {},
				success: function(data){
					console.log(data)
					updateLike(this_, data.count, data.liked)

				}, error: function(error){
					console.log(error)
				}

			});
		});
	});