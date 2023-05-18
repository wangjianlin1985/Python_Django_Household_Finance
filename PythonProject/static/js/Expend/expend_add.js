$(function () {
	$("#expend_expendPurpose").validatebox({
		required : true, 
		missingMessage : '请输入支出用途',
	});

	$("#expend_payAccount").validatebox({
		required : true, 
		missingMessage : '请输入支付账号',
	});

	$("#expend_expendMoney").validatebox({
		required : true,
		validType : "number",
		missingMessage : '请输入支付金额',
		invalidMessage : '支付金额输入不对',
	});

	$("#expend_expendDate").datebox({
	    required : true, 
	    showSeconds: true,
	    editable: false
	});

	//单击添加按钮
	$("#expendAddButton").click(function () {
		//验证表单 
		if(!$("#expendAddForm").form("validate")) {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		} else {
			$("#expendAddForm").form({
			    url:"/Expend/add",
				queryParams: {
			    	"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
			    onSubmit: function(){
					if($("#expendAddForm").form("validate"))  { 
	                	$.messager.progress({
							text : "正在提交数据中...",
						}); 
	                	return true;
	                } else {
	                    return false;
	                }
			    },
			    success:function(data){
			    	$.messager.progress("close");
                    //此处data={"Success":true}是字符串
                	var obj = jQuery.parseJSON(data); 
                    if(obj.success){ 
                        $.messager.alert("消息","保存成功！");
                        $(".messager-window").css("z-index",10000);
                        $("#expendAddForm").form("clear");
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    }
			    }
			});
			//提交表单
			$("#expendAddForm").submit();
		}
	});

	//单击清空按钮
	$("#expendClearButton").click(function () { 
		//$("#expendAddForm").form("clear"); 
		location.reload()
	});
});
