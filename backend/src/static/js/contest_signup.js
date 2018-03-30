$(document).ready(function(){
    	function updateLike(btn, newCount, verb){
    		if(verb){
    			btn.text(newCount + " " + "Unlike");
    		}
    		else{
    			btn.text(newCount + " " + "Like");
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