$(function () {
	$("#income_incomeFrom").validatebox({
		required : true, 
		missingMessage : '请输入收入来源',
	});

	$("#income_payAccount").validatebox({
		required : true, 
		missingMessage : '请输入支付账号',
	});

	$("#income_incomeMoney").validatebox({
		required : true,
		validType : "number",
		missingMessage : '请输入收入金额',
		invalidMessage : '收入金额输入不对',
	});

	$("#income_incomeDate").datebox({
	    required : true, 
	    showSeconds: true,
	    editable: false
	});

	//单击添加按钮
	$("#incomeAddButton").click(function () {
		//验证表单 
		if(!$("#incomeAddForm").form("validate")) {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		} else {
			$("#incomeAddForm").form({
			    url:"/Income/add",
				queryParams: {
			    	"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
			    onSubmit: function(){
					if($("#incomeAddForm").form("validate"))  { 
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
                        $("#incomeAddForm").form("clear");
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    }
			    }
			});
			//提交表单
			$("#incomeAddForm").submit();
		}
	});

	//单击清空按钮
	$("#incomeClearButton").click(function () { 
		//$("#incomeAddForm").form("clear"); 
		location.reload()
	});
});
