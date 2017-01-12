'use strict';

function add_edit_doc_title_listener() {
    // change document title
    $(".edit_doc_title_button").on("click", function() {
        var $td = $(this).parents("td");
        var orig_doc_title = $td.find("span").text();
        $td.html("<input type='text'></input><i class='fa fa-check-circle' style='cursor: pointer' aria-hidden='true'></i>");
        if (user_dashboard_page_type == "administrated_coterie_page")
            $td.find("input").css("width", "80px");
        $td.find("input").val(orig_doc_title);
        $td.find("i").on("click", function() {
            var new_doc_title = $td.find("input").val();
            if (new_doc_title != orig_doc_title) {

                if (user_dashboard_page_type == "documents_page")
                    var action = "/file_viewer/edit_doc_title";
                else if (user_dashboard_page_type == "administrated_coterie_page")
                    var action = "/coterie/edit_coteriedoc_title";

                $.ajax({
                    type: "POST",
                    url: action,
                    data: {
                        csrfmiddlewaretoken: getCookie('csrftoken'),
                        document_id: $td.parents("tr").find("input[name='document_id']").val(),
                        new_doc_title: new_doc_title,
                    },
                });
            }
            $td.html('<span>' + new_doc_title + '</span>\
                      <i class="fa fa-pencil-square edit_doc_title_button" style="cursor: pointer" aria-hidden="true"></i>');
            add_edit_doc_title_listener();
        });
    });
}

$(document).ready(function() {
    $(".pe-7s-plus").on("click", function() {
        var create_group_form_layer = layer.open({
            type: 1,
            title: "Create a new group",
            skin: 'layui-layer-demo',
            closeBtn: 1,
            shift: 4,
            area: ['380px', '280px'],
            shadeClose: true, //开启遮罩关闭
            content: '\
                <form id="create_group_form" style="margin-left: auto; margin-right: auto; margin-top: 28px; width: 200px;">\
                    <input name="coterie_name" type="text" class="form-control" placeholder="name"><br>\
                    <textarea name="coterie_description" type="text" class="form-control" rows="2" placeholder="description"></textarea><br>\
                    <button class="btn btn-info" type="button" style="float: right;">create</button>\
                </form>\
            '
        });

        $("#create_group_form").find("button").on("click", function() {
            var $form = $("#create_group_form");
            $(this).css("disabled", "true");
            $.ajax({
                type: "POST",
                url: "/coterie/handle_create_coterie",
                data: {
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                    coterie_name: $form.find("input").val(),
                    coterie_description: $form.find("textarea").val(),
                },
                success: function () {
                    layer.close(create_group_form_layer);
                    window.location.reload();
                },
            });
        });
    });

    // add indexes for table
    $("tbody").each(function() {
        var $tbody = $(this);
        var length = $tbody.children("tr").length;     
        for (var i = 0; i < length; i++) {
            $($tbody.children("tr")[i]).children("td:first").text(i + 1);
        }
    });

    // confirmation after clicking delete
    $(".file_delete_form").find("button").on("click", function() {
        var this_button = $(this);
        layer.confirm('confirm delete?', 
            {
                btn: ['yes'], //按钮
                title: false,
                shadeClose: true, //开启遮罩关闭
            }, 
            function() {
                layer.msg('delete successfully', {icon: 1});
                this_button.parents(".file_delete_form").submit();
            }
        );
    });
    // confirmation after clicking remove member
    $(".member_remove_form").find("button").on("click", function() {
        var this_button = $(this);
        layer.confirm('confirm remove this member?', 
            {
                btn: ['yes'], //按钮
                title: false,
                shadeClose: true, //开启遮罩关闭
            }, 
            function() {
                layer.msg('remove successfully', {icon: 1});
                this_button.parents(".member_remove_form").submit();
            }
        );
    });

    add_edit_doc_title_listener();
});

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
