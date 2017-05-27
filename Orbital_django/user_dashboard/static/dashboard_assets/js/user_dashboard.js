'use strict';

function addEditDocTitleListener() {
    // change document title
    $(".EditDocTitleButton").on("click", function() {
        var $td = $(this).parents("td");
        var origDocTitle = $td.find("span").text();
        $td.html("<input type='text'></input>&nbsp<i class='fa fa-check-circle' style='cursor: pointer' aria-hidden='true'></i>");
        if (userDashboardPageType == "administrated_coterie_page")
            $td.find("input").css("width", String($td.width() - $td.find("i").width() - 80) + "px");
        else
            $td.find("input").css("width", String($td.width() - $td.find("i").width() - 28) + "px");
        $td.find("input").val(origDocTitle);

        $td.find("i").on("click", function() {
            var new_doc_title = $td.find("input").val();
            if (new_doc_title != origDocTitle) {

                if (userDashboardPageType == "documents_page")
                    var action = "/file_viewer/edit_doc_title";
                else if (userDashboardPageType == "administrated_coterie_page")
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
            $td.html('<i class="fa fa-pencil-square-o EditDocTitleButton" style="cursor: pointer" aria-hidden="true"></i>&nbsp' + '<span>' + new_doc_title + '</span>');
            addEditDocTitleListener();
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
    $(".FileDeleteForm").find("button").on("click", function() {
        var this_button = $(this);
        layer.confirm('confirm delete?', 
            {
                btn: ['yes'], //按钮
                title: false,
                shadeClose: true, //开启遮罩关闭
            }, 
            function() {
                layer.msg('delete successfully', {icon: 1});
                this_button.parents(".FileDeleteForm").submit();
            }
        );
    });
    // confirmation after clicking remove member
    $(".MemberRemoveForm").find("button").on("click", function() {
        var this_button = $(this);
        layer.confirm('confirm remove this member?', 
            {
                btn: ['yes'], //按钮
                title: false,
                shadeClose: true, //开启遮罩关闭
            }, 
            function() {
                layer.msg('remove successfully', {icon: 1});
                this_button.parents(".MemberRemoveForm").submit();
            }
        );
    });

    addEditDocTitleListener();
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
