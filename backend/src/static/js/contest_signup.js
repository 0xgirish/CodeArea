$(document).ready(function(){
    	function updateStatus(btn, verb){
    		if(verb){
    			btn.text("Signed Up");
    		}
    	}
		$(".signup-btn").click(function(e){
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
					updateStatus(this_, data.signup)

				}, error: function(error){
					console.log(error)
				}

			});
		});
	});