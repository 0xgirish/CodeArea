$(document).ready(function() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE') {
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        }
    });

    function update(btn, newCount, verb) {
        btn.closest('tr').remove();
    }
    $(".p-del").click(function(e) {
        e.preventDefault();
        var this_ = $(this);
        var likeUrl = "http://127.0.0.1:8000/contests/api/contest-problem/c/" + this_.attr("data-id") + "/";

        console.log(likeUrl)
        $.ajax({
            url: likeUrl,
            method: "DELETE",
            data: {
                somedata: 'somedata',
                moredata: 'moredata',
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(data) {
                console.log(data)
                update(this_, data.count, data.liked)

            },
            error: function(error) {
                console.log(error)
            }

        });
    });
});