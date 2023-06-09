$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/ExpendType/update/" + $("#expendType_expendTypeId_modify").val(),
		type : "get",
		data : {
			//expendTypeId : $("#expendType_expendTypeId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (expendType, response, status) {
			$.messager.progress("close");
			if (expendType) { 
				$("#expendType_expendTypeId_modify").val(expendType.expendTypeId);
				$("#expendType_expendTypeId_modify").validatebox({
					required : true,
					missingMessage : "请输入支出类型id",
					editable: false
				});
				$("#expendType_expendTypeName_modify").val(expendType.expendTypeName);
				$("#expendType_expendTypeName_modify").validatebox({
					required : true,
					missingMessage : "请输入支出类型名称",
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#expendTypeModifyButton").click(function(){ 
		if ($("#expendTypeModifyForm").form("validate")) {
			$("#expendTypeModifyForm").form({
			    url:"ExpendType/update/" + $("#expendType_expendTypeId_modify").val(),
			    onSubmit: function(){
					if($("#expendTypeEditForm").form("validate"))  {
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
                	var obj = jQuery.parseJSON(data);
                    if(obj.success){
                        $.messager.alert("消息","信息修改成功！");
                        $(".messager-window").css("z-index",10000);
                        //location.href="frontlist";
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    } 
			    }
			});
			//提交表单
			$("#expendTypeModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
