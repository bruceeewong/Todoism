$(document).ready(function () {
    var ENTER_KEY = 13;
    var ESC_KEY = 27;

    // 定义 ajax 错误事件处理函数
    $(document).ajaxError(function (event, request) {
        var message = null;

        if (request.responseJSON && request.responseJSON.hasOwnProperty('message')) {
            message = request.responseJSON.message;
        } else if (request.responseText) {
            var IS_JSON = true;
            try {
                var data = JSON.parse(request.responseText);
            }
            catch (err) {
                IS_JSON = false;
            }

            if (IS_JSON && data !== undefined && data.hasOwnProperty('message')) {
                message = JSON.parse(request.responseText).message;
            } else {
                message = default_error_message;
            }
        } else {
            message = default_error_message;
        }
        M.toast({html: message});
    });

    // 配置 ajax
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            // 除了GET|HEAD|OPTIONS|TRACE, 其他请求都要附带 csrf_token
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        }
    });

    // 绑定 hashchange 回调函数, 实现单页应用效果
    $(window).bind('hashchange', function () {
        // 有些浏览器会连同#返回一起返回, 而有些则不
        var hash = window.location.hash.replace('#', '');
        var url = null;
        if (hash === 'login') {
            url = login_page_url
        } else if (hash === 'app') {
            url = app_page_url
        } else {
            // 默认视图为intro
            // 这里包括hash为空或者hash对应页面找不到, 都会回到intro
            url = intro_page_url
        }

        // 请求hash对应的HTML资源
        $.ajax({
            type: 'GET',
            url: url,
            success: function (data) {
                $('#main').hide().html(data).fadeIn(800); // 将返回的html插入 main 节点
                activeM();
            }
        });
    });

    // 设置初次打开页面的逻辑
    // 如果没有hash则加载默认视图 #intro, 否则加载hash对应的视图
    if (window.location.hash === '') {
        window.location.hash = '#intro'; // home page, show the default view
    } else {
        $(window).trigger('hashchange'); // user refreshed the browser, fire the appropriate function
    }

    // 切换密码输入框的可见性
    function toggle_password() {
        var password_input = document.getElementById('password-input');
        if (password_input.type === 'password') {
            password_input.type = 'text';
        } else {
            password_input.type = 'password';
        }
    }
    $(document).on('click', '#toggle-password', toggle_password);

    function display_dashboard() {
        var all_count = $('.item').length;
        if (all_count === 0) {
            $('#dashboard').hide();
        } else {
            $('#dashboard').show();
            $('ul.tabs').tabs();
        }
    }

    // TODO: 激活 app 页面?
    function activeM() {
        $('.sidenav').sidenav();
        $('ul.tabs').tabs();
        $('.modal').modal();
        $('.tooltipped').tooltip();
        $('.dropdown-trigger').dropdown({
                constrainWidth: false,
                coverTrigger: false
            }
        );
        display_dashboard();
    }

    // 移除 edit 输入框
    function remove_edit_input() {
        var $edit_input = $('#edit-item-input');
        $edit_input.parent().prev().show();
        $edit_input.parent().remove();
    }

    // 重置各个count的数字
    function refresh_count() {
        var $items = $('.item');

        display_dashboard();
        var all_count = $items.length;
        var active_count = $items.filter(function () {
            return $(this).data('done') === false;
        }).length;
        var completed_count = $items.filter(function () {
            return $(this).data('done') === true;
        }).length;
        $('#all-count').html(all_count);
        $('#active-count').html(active_count);
        $('#active-count-nav').html(active_count);
        $('#completed-count').html(completed_count);
    }

    // 新增 item 函数
    function new_item(e) {
        var $input = $('#item-input');
        var value = $input.val().trim();
        if (e.which !== ENTER_KEY || !value) {
            return;
        }
        $input.focus().val('');
        $.ajax({
            type: 'POST',
            url: new_item_url,
            data: JSON.stringify({'body': value}),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                M.toast({html: data.message, classes: 'rounded'});

                // 将新增的元素的html插到最后
                $('.items').append(data.html);
                activeM();
                refresh_count();
            }
        });
    }

    // 编辑 item 函数
    function edit_item(e) {
        var $edit_input = $('#edit-item-input');
        var value = $edit_input.val().trim();
        if (e.which !== ENTER_KEY || !value) {
            return;
        }
        $edit_input.val('');

        if (!value) {
            M.toast({html: empty_body_error_message});
            return;
        }

        var url = $edit_input.parent().prev().data('href');
        var id = $edit_input.parent().prev().data('id');

        $.ajax({
            type: 'PUT',
            url: url,
            data: JSON.stringify({'body': value}),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                // 后端告知更新成功时, 可直接拿输入框的值更新UI
                $('#body' + id).html(value); // 更新item的body显示值
                $edit_input.parent().prev().data('body', value); // 更新item的body绑定值
                remove_edit_input(); // 移除输入框换成普通div
                M.toast({html: data.message});
            }
        })
    }

    // add new item
    $(document).on('keyup', '#item-input', new_item.bind(this));

    // edit item
    $(document).on('keyup', '#edit-item-input', edit_item.bind(this));

    $(document).on('click', '.done-btn', function () {
        var $item = $(this).parent().parent();
        var $this = $(this);

        if ($item.data('done')) {
            $.ajax({
                type: 'PATCH',
                url: $this.data('href'),
                success: function (data) {
                    $this.next().removeClass('inactive-item');
                    $this.next().addClass('active-item');
                    $this.find('i').text('check_box_outline_blank');
                    $item.data('done', false);
                    M.toast({html: data.message});
                    refresh_count();
                }
            })
        } else {
            $.ajax({
                type: 'PATCH',
                url: $this.data('href'),
                success: function (data) {
                    $this.next().removeClass('active-item');
                    $this.next().addClass('inactive-item');
                    $this.find('i').text('check_box');
                    $item.data('done', true);
                    M.toast({html: data.message});
                    refresh_count();
                }
            })

        }
    });

    // .item 类的元素, 编辑按钮平时隐藏, 悬浮时出现
    $(document)
        .on('mouseenter', '.item', function () {
            $(this).find('.edit-btns').removeClass('hide');
        })
        .on('mouseleave', '.item', function () {
            $(this).find('.edit-btns').addClass('hide');
        });

    // 点击 edit btn 响应事件
    $(document).on('click', '.edit-btn', function () {
        // 先获取绑在.item上的id 与 body
        var $item = $(this).parent().parent();
        var itemId = $item.data('id');
        var itemBody = $('#body' + itemId).text();

        // 再隐藏原来的元素, 替换成一个输入框
        $item.hide();
        $item.after('<div class="row card-panel hoverable">' +
                '<input class="validate" id="edit-item-input" type="text" value="' + itemBody +
                '" autocomplete="off" autofocus required>' +
                '</div>');

        var $edit_input = $('#edit-item-input');

        // *2 是为了让光标 focus 在文字后
        // Opera sometimes sees a carriage return as 2 characters.
        var strLength = $edit_input.val().length * 2;

        $edit_input.focus();
        $edit_input[0].setSelectionRange(strLength, strLength);

        // 移除 edit form 当按下 ESC 或 focus out.
        $(document).on('keydown', function (e) {
            if (e.keyCode === ESC_KEY) {
                remove_edit_input();
            }
        });

        $edit_input.on('focusout', function () {
            remove_edit_input();
        });
    });

    $(document).on('click', '.delete-btn', function () {
        var $item = $(this).parent().parent();
        $.ajax({
            type: 'DELETE',
            url: $(this).data('href'),
            success: function (data) {
                $item.remove();
                activeM();
                refresh_count();
                M.toast({html: data.message});
            }
        });
    });


    /**
     *  注册模块
     *  此处是后端返回随机账户和密码, 所以直接 GET
     */
    function register() {
        $.ajax({
            type: 'GET',
            url: register_url,
            success: function (data) {
                $('#username-input').val(data.username);
                $('#password-input').val(data.password);
                M.toast({html: data.message})
            }
        });
    }
    // 注册按钮点击响应事件
    $(document).on('click', '#register-btn', register);

    /**
     *  登录模块
     */
    function login_user() {
        var username = $('#username-input').val();
        var password = $('#password-input').val();
        if (!username || !password) {
            M.toast({html: login_error_message});
            return;
        }

        var data = {
            'username': username,
            'password': password
        };
        $.ajax({
            type: 'POST',
            url: login_url,
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                // 登录成功, 跳转到 app 页
                if (window.location.hash === '#app' || window.location.hash === 'app') {
                    $(window).trigger('hashchange');
                } else {
                    window.location.hash = '#app';
                }
                activeM();
                M.toast({html: data.message});
            }
        });
    }
    // 登录输入框回车响应事件
    $(document).on('keyup', '.login-input', function (e) {
        if (e.which === ENTER_KEY) {
            login_user();
        }

    });
    // 登录按钮点击响应事件
    $(document).on('click', '#login-btn', login_user);
    // 登出事件
    $(document).on('click', '#logout-btn', function () {
        $.ajax({
            type: 'GET',
            url: logout_url,
            success: function (data) {
                window.location.hash = '#intro';
                activeM();
                M.toast({html: data.message});
            }
        });
    });

     // 点击 Tab栏 未完成
    $(document).on('click', '#active-item', function () {
        var $items = $('.item');
        $items.show();
        // 隐藏已完成的
        $items.filter(function () {
            return $(this).data('done');
        }).hide();
    });

    // 点击 Tab栏 已完成
    $(document).on('click', '#completed-item', function () {
        var $items = $('.item');
        $items.show();
        // 隐藏未完成的
        $items.filter(function () {
            return !$(this).data('done');
        }).hide();
    });

    // 点击 Tab栏 所有
    $(document).on('click', '#all-item', function () {
        $('#item-input').focus();
        $('.item').show();
    });

    // 点击清除按钮响应函数
    $(document).on('click', '#clear-btn', function () {
        var $items = $('.item');
        $.ajax({
            type: 'DELETE',
            url: clear_item_url,
            success: function (data) {
                $items.filter(function () {
                    return $(this).data('done');
                }).remove();
                M.toast({html: data.message, classes: 'rounded'});
                refresh_count();
            }
        });
    });

    $(document).on('click', '.lang-btn', function () {
        $.ajax({
            type: 'GET',
            url: $(this).data('href'),
            success: function (data) {
                $(window).trigger('hashchange');
                activeM();
                M.toast({html: data.message});
            }
        });
    });

    activeM();  // initialize Materialize
});
