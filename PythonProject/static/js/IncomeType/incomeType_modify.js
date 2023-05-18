$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/IncomeType/update/" + $("#incomeType_typeId_modify").val(),
		type : "get",
		data : {
			//typeId : $("#incomeType_typeId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (incomeType, response, status) {
			$.messager.progress("close");
			if (incomeType) { 
				$("#incomeType_typeId_modify").val(incomeType.typeId);
				$("#incomeType_typeId_modify").validatebox({
					required : true,
					missingMessage : "请输入分类id",
					editable: false
				});
				$("#incomeType_typeName_modify").val(incomeType.typeName);
				$("#incomeType_typeName_modify").validatebox({
					required : true,
					missingMessage : "请输入分类名称",
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#incomeTypeModifyButton").click(function(){ 
		if ($("#incomeTypeModifyForm").form("validate")) {
			$("#incomeTypeModifyForm").form({
			    url:"IncomeType/update/" + $("#incomeType_typeId_modify").val(),
			    onSubmit: function(){
					if($("#incomeTypeEditForm").form("validate"))  {
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
			$("#incomeTypeModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
