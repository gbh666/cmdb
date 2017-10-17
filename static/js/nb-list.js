/**
 * Created by DELL on 2017/10/11.
 */
(function (jq) {


    // 请求路径
    var requestUrl = "";
    var GLOBAL_CHOICES_DICT = {
        // 'status_choices': [[0,'上架'],[1,'上线']] JSON之后都变成列表
        // 'xxxx_choices': [[0,'xxx'],]
    };

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            // 请求头中设置一次csrf-token
            if(!csrfSafeMethod(settings.type)){
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    });

    function getChoicesNameById(choice_name, id) {
        // 根据状态id取到对应中文
        var val;

        var status_choices_list = GLOBAL_CHOICES_DICT[choice_name]; // 拿到所有的状态列表
        $.each(status_choices_list, function (kkkk, vvvv) {  // kkkk:索引，vvvv：每个状态列表[0,'上架']|[1,'上线']
            if (id == vvvv[0]) {   //如果状态id对应某个状态，返回这个状态的中文
                val = vvvv[1];
            }
        });
        return val;
    }

    // 自定义format方法
    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s, i) {
            return args[i];
        });
    };

    //向后台获取数据
    function init(pageNum) {
        var condition = {};
        $('#loading').removeClass('hide'); //加载中图标
        if ($('#doSearch').attr('searching')) {
            condition = getSearchCondition();
            // $('#doSearch').removeAttr('searching')
        }
        $.ajax({
            url: requestUrl,
            type: 'GET',
            data: {'pageNum': pageNum, 'condition': JSON.stringify(condition)},
            dataType: 'JSON',
            success: function (response) {
                //处理choice
                initChoices(response.global_choices_dict);
                //处理表头
                initTableHead(response.table_config);
                //处理表内容
                initTableBody(response.data_list, response.table_config);
                // 处理页码html
                initPageHtml(response.page_html);

                initSearchCondition(response.search_config);
                $('#loading').addClass('hide')
            },
            error: function () {
                $('#loading').addClass('hide')
            }
        })
    }

    function bindSearchConditionEvent() {
        /* 改变下拉框内容时*/
        $('#searchCondition').on('click', 'li', function () {
            // $(this) = li标签

            // 找到文本修改
            $(this).parent().prev().prev().text($(this).text());

            // 找input标签，修改，重建
            $(this).parent().parent().next().remove();

            var name = $(this).find('a').attr('name');
            var type = $(this).find('a').attr('type');
            if (type == 'select') {
                var choice_name = $(this).find('a').attr('choice_name');

                // 作业：生成下拉框，
                var tag = document.createElement('select');
                tag.className = "form-control no-radius";
                tag.setAttribute('name', name);
                $.each(GLOBAL_CHOICES_DICT[choice_name], function (i, item) {
                    var op = document.createElement('option');
                    op.innerHTML = item[1];
                    op.setAttribute('value', item[0]);
                    $(tag).append(op);
                })
            } else {
                // <input class="form-control no-radius" placeholder="逗号分割多条件" name="hostnmae">
                var tag = document.createElement('input');
                tag.setAttribute('type', 'text');
                // $(tag).addClass('form-control no-radius')
                tag.className = "form-control no-radius";
                tag.setAttribute('placeholder', '请输入条件');
                tag.setAttribute('name', name);
            }

            $(this).parent().parent().after(tag);

        });

        /* 添加搜索条件 */
        $('#searchCondition .add-condition').click(function () {

            var $condition = $(this).parent().parent().clone();
            $condition.find('.add-condition').removeClass('add-condition').addClass('del-condition').find('i').attr('class', 'fa fa-minus-square');

            // $(this).parent().parent().parent().append($condition);
            // $('#searchCondition').append($condition);
            $condition.appendTo($('#searchCondition'));
        });

        /* 删除搜索条件 */
        $('#searchCondition').on('click', '.del-condition', function () {
            $(this).parent().parent().remove();
        });

        /* 点击搜索按钮 */
        $('#doSearch').click(function () {
            $('#doSearch').attr('searching', 'true');
            init(1);
        })

    }

    function initSearchCondition(searchConfig) {
        if (!$('#searchCondition').attr('init')) {
            var $ul = $('#searchCondition :first').find('ul');
            $ul.empty();

            initDefaultSearchCondition(searchConfig[0]);

            $.each(searchConfig, function (i, item) {
                var li = document.createElement('li');
                var a = document.createElement('a');
                a.innerHTML = item.title;
                a.setAttribute('name', item.name);
                a.setAttribute('type', item.type);
                if (item.type == 'select') {
                    a.setAttribute('choice_name', item.choice_name);
                }
                $(li).append(a);
                $ul.append(li)
            });
            $('#searchCondition').attr('init', 'true');
        }


    }

    function initDefaultSearchCondition(item) {

        // item={'name': 'hostname','title':'主机名','type':'input'},
        if (item.type == 'input') {
            var tag = document.createElement('input');
            tag.setAttribute('type', 'text');
            // $(tag).addClass('form-control no-radius')
            tag.className = "form-control no-radius";
            tag.setAttribute('placeholder', '请输入条件');
            tag.setAttribute('name', item.name);
        }

        else {
            var tag = document.createElement('select');
            tag.className = "form-control no-radius";
            tag.setAttribute('name', item.name);
            $.each(GLOBAL_CHOICES_DICT[item.choice_name], function (i, row) {
                var op = document.createElement('option');
                op.innerHTML = row[1];
                op.setAttribute('value', row[0]);
                $(tag).append(op);
            })
        }

        $('#searchCondition').find('.input-group').append(tag);
        $('#searchCondition').find('.input-group label').text(item.title);
    }

    function getSearchCondition() {
        // 找所有input,select
        // 作业：result数据格式为：
        /*
         {
         server_status_id: [1,2],
         hostname: ['c1.com','c2.com']
         }
         */
        var result = {};
        $('#searchCondition').find('input[type="text"],select').each(function () {
            var name = $(this).attr('name');
            var val = $(this).val();
            result[name] = val
        });
        return result;

    }

    function initChoices(global_choices_dict) {
        GLOBAL_CHOICES_DICT = global_choices_dict
    }

    function initPageHtml(page_html) {
        $('#pagination').empty().append(page_html)
    }

    function initTableHead(table_config) {
        //处理表头的函数，table_config：配置信息
        $('#tHead tr').empty();
        $.each(table_config, function (k, conf) {
            if (conf.display) {
                var th = document.createElement('th');
                th.innerHTML = conf.title;
                $('#tHead tr').append(th);
            }
        });
    }

    function initTableBody(data_list, table_config) {
        // 处理表内容
        //data_list：数据库中取到的所需内容，table_config：表格配置信息
        $('#tBody').empty();
        $.each(data_list, function (k, row_dict) {
            // 循环数据库中取到的列表
            // 每个row_dict:{'hostname':'xx','sn':xx,'os_platform':'xxx'}
            var tr = document.createElement('tr');
            $.each(table_config, function (kk, vv) { //kk：索引，vv：每个配置字典
                /*table_config = [
                 {
                 'q': None,
                 'title': '选择',
                 'text': {'tpl':'<input type="checkbox" value="{nid}" />','kwargs':{'nid': '@id' }},
                 },
                 {
                 'q': 'id',
                 'title': 'ID',
                 'text': {'tpl': '{a1}', 'kwargs': {'a1': '@id'}},
                 },]*/
                if (vv.display) {
                    var td = document.createElement('td');
                    var format_dict = {}; //格式化用到的字典

                    // 循环每个字典的kwargs，把带有@符号的值替换为数据库中的值，
                    // 带有@@的值去GLOBAL_CHOICES_DICT中找到对应的状态列表，根据状态id替换对应中文，其他不变
                    $.each(vv.text.kwargs, function (kkk, vvv) { //kkk：键，vvv：值(@id|@hostname|@@status_choices)
                        if (vvv.substring(0, 2) == "@@") {

                            var name = vvv.substring(2, vvv.length); // status_choices
                            var val = getChoicesNameById(name, row_dict[vv.q]);
                            format_dict[kkk] = val;
                        }
                        else if (vvv[0] == "@") {
                            var name = vvv.substring(1, vvv.length);
                            format_dict[kkk] = row_dict[name];
                        } else {
                            format_dict[kkk] = vvv;
                        }
                    });

                    // 循环给td标签添加属性
                    $.each(vv.attr, function (attrKey, attrVal) { //k1:键，v1：值
                        if (attrVal[0] == '@') {
                            attrVal = row_dict[attrVal.substring(1, attrVal.length)];
                        }
                        td.setAttribute(attrKey, attrVal);

                    });

                    // 拿到信息格式化到对应的模板中
                    td.innerHTML = vv.text.tpl.format(format_dict);
                    $(tr).append(td)
                }

            });

            $('#tBody').append(tr);
        })
    }

    function tdIntoEditMode($td) {
        if ($('#editModeStatus').hasClass('btn-warning')) {
            if ($td.attr('edit-type') == 'select') {
                var choiceKey = $td.attr('choice-key');
                var origin = $td.attr('origin');
                // GLOBAL_CHOICES_DICT[choiceKey]
                /*
                 [
                 [1,'xxx'],
                 [2,'xxx'],
                 [3,'xxx'],
                 ]
                 */
                var tag = document.createElement('select');
                tag.className = 'form-control';
                $.each(GLOBAL_CHOICES_DICT[choiceKey], function (k, value) {
                    var op = document.createElement('option');
                    op.innerHTML = value[1];
                    op.value = value[0];
                    if (value[0] == origin) {
                        op.setAttribute('selected', 'selected');
                    }
                    tag.appendChild(op);
                    // // $(tag).append(op);
                });
                $td.html(tag);
            }
            else {
                // input
                var text = $td.text();
                var tag = document.createElement('input');
                tag.setAttribute('type', 'text');
                tag.className = 'form-control';
                tag.value = text;
                $td.html(tag);
            }
        }

    }

    function tdOutEditMode($td) {
        var editStatus = false;

        var origin = $td.attr('origin');

        if($td.attr('edit-type') == 'select'){
            var val = $td.find('select').val();
            // var text = $td.find('select')[0].selectedOptions[0].innerText;
            var text = $td.find('select option[value="'+ val +'"]').text();
            $td.attr('new-value',val);
            $td.html(text);

        }else{
            var val = $td.find('input').val();
            $td.html(val);
        }

        if(origin != val){
            editStatus = true;
        }
        return editStatus;
    }

    function trIntoEditMode($tr) {
        $tr.addClass('success');
        $tr.find('td[edit="true"]').each(function () {
            // $(this)，需要进入编辑模式的td标签
            tdIntoEditMode($(this));
        })
    }

    function trOutEditMode($tr) {
        $tr.removeClass('success');
        $tr.find('td[edit="true"]').each(function () {
            // $(this)，需要退出编辑模式的td标签
            if (tdOutEditMode($(this))) {
                $tr.attr('edit-status', 'true');
            }
        })
    }

    function bindEditModeEvent() {
        $('#tBody').on('click', ':checkbox', function () {
            if($('#editModeStatus').hasClass('btn-warning')) {
                // $(this)，当前checkbox标签
                if ($(this).prop('checked')) {
                    // 进入编辑模式
                    // 如果后台配置文件：edit=true
                    var $tr = $(this).parent().parent();
                    $tr.addClass('success');
                    $tr.find('td[edit="true"]').each(function () {
                        // $(this),需要进入编辑模式的td标签
                        tdIntoEditMode($(this))
                    })
                }
                else {
                    // 退出编辑模式
                    var $tr = $(this).parent().parent();
                    $tr.removeClass('success');
                    $tr.find('td[edit="true"]').each(function () {
                        // $(this),需要退出编辑模式的td标签
                        if (tdOutEditMode($(this))) {
                            $tr.attr('edit-status', 'true');
                        }
                    })
                }
            }
        })
    }

    function bindBtnGroupEvent() {
        // 进入和退出编辑模式
        $('#editModeStatus').click(function () {
            if ($(this).hasClass('btn-warning')) {
                // 需要退出编辑模式
                $(this).removeClass('btn-warning');
                $(this).text('进入编辑模式');
                $('#tBody :checked').each(function () {
                    var $tr = $(this).parent().parent();
                    trOutEditMode($tr);
                })
            } else {
                $(this).addClass('btn-warning');
                $(this).text('退出编辑模式');
                $('#tBody :checked').each(function () {
                    var $tr = $(this).parent().parent();
                    trIntoEditMode($tr);
                })
            }
        });

        // 全选
        $('#checkAll').click(function () {
            $('#tBody :checkbox').each(function () {
                if(!$(this).prop('checked')){
                    // 选中
                    $(this).prop('checked','true');
                    // 进入编辑模式
                    if($('#editModeStatus').hasClass('btn-warning')){
                        var $tr = $(this).parent().parent();
                        trIntoEditMode($tr);
                    }
                }
            })
        });

        // 反选
        $('#checkReverse').click(function () {
            $('#tBody :checkbox').each(function () {
                if(!$(this).prop('checked')){
                    // 未选中的
                    $(this).prop('checked',true);
                    if($('#editModeStatus').hasClass('btn-warning')){
                        var $tr = $(this).parent().parent();
                        trIntoEditMode($tr);
                    }
                }else {
                    // 已经选中的
                    $(this).prop('checked',false);
                    if($('#editModeStatus').hasClass('btn-warning')){
                        var $tr = $(this).parent().parent();
                        trOutEditMode($tr);
                    }
                }
            })
        });

        // 取消
        $('#checkCancle').click(function () {
            $('#tBody :checkbox').each(function () {
                if($(this).prop('checked')){
                    // 取消选中
                    $(this).prop('checked',false);
                    // 退出编辑模式
                    if($('#editModeStatus').hasClass('btn-warning')){
                        var $tr = $(this).parent().parent();
                        trOutEditMode($tr);
                    }
                }
            })
        });

        // 删除
        $('#delMulti').click(function () {
            // 显示模态对话框
            // 给确定按钮绑定事件
            var ids = [];
            // 把需要删除记录的id添加到列表
            $('#tBody :checked').each(function () {
                ids.push($(this).val());
            });

            $.ajax({
                url:requestUrl,
                type:'delete',
                data:JSON.stringify(ids),
                traditional:true,
                dataType:'JSON',
                success:function (arg) {
                    if(arg.status){
                        // 显示正确信息
                        $('#handleStatus').html('执行成功');
                        $('#tBody :checked').each(function () {
                           $(this).parent().parent().remove();
                        });
                        setTimeout(function () {
                            $('#handleStatus').empty();
                        },5000)
                    }else {
                        // 显示错误信息
                        $('#handleStatus').html(arg.msg);
                        setTimeout(function () {
                            $('#handleStatus').empty();
                        },5000)
                    }
                }

            })

        });

        // 保存
        $('#saveMulti').click(function () {
            var update_dict = [
                // {'nid':1, 'hostname': 'c1.com'},
                // {'nid':2, 'hostname': 'c1.com'},
                // {'nid':3, 'hostname': 'c1.com'},
            ];

            $('#tBody tr[edit-status="true"]').each(function () {
                // $(this),是每一个tr标签
                var tmp = {};
                tmp['nid'] = $(this).children().first().attr('nid');

                $(this).children('[edit="true"]').each(function () {
                    // $(this)，是td
                    var name = $(this).attr('name');
                    var origin = $(this).attr('origin');

                    if($(this).attr('edit-type') == 'select'){

                        var new_val = $(this).attr('new-value');
                    }else {
                        var new_val = $(this).text();
                    }

                    if(origin != new_val){
                        tmp[name] = new_val
                    }

                });
                update_dict.push(tmp)
            });
            console.log(update_dict);
            // 数据发送到后台PUT
            $.ajax({
                url:requestUrl,
                type:'put',
                data:JSON.stringify(update_dict),
                traditional:true,
                dataType:'JSON',
                success:function (arg) {
                    if(arg.status){
                        // 显示正确信息
                        $('#handleStatus').html('执行成功');
                        setTimeout(function () {
                            $('#handleStatus').empty();
                        },5000)
                    }else {
                        // 显示错误信息
                        $('#handleStatus').html(arg.msg);
                        setTimeout(function () {
                            $('#handleStatus').empty();
                        },5000)
                    }
                }
            })
        })
    }

    ctrlStatus = false;

    window.onkeydown = function (event) {
        if(event && event.keyCode == 17){
            ctrlStatus = true;
        }
    };

    window.onkeyup = function (event) {
        if(event && event.keyCode == 17){
            ctrlStatus = false;
        }
    };

    function bindSelectChangeEvent() {
        $('#tBody').on('change','select',function () {
            if(ctrlStatus){
                var v = $(this).val();
                var $tr = $(this).parent().parent();
                var index = $(this).parent().index();

                $tr.nextAll().each(function () {
                    if($(this).find(':checkbox').prop('checked')){
                        // 选择
                        $(this).children().eq(index).children().val(v);
                    }
                })
            }
        })
    }

    // 使jQuery对象下都有一个nBList方法
    jq.extend({
        "nBList": function (url) {
            requestUrl = url;
            init(1);
            bindSearchConditionEvent();
            bindEditModeEvent();
            bindBtnGroupEvent();
            bindSelectChangeEvent();
        },
        "changePage": function (pageNum) {
            init(pageNum);
        }
    });

})(jQuery);
