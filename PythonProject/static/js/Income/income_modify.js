$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/Income/update/" + $("#income_incomeId_modify").val(),
		type : "get",
		data : {
			//incomeId : $("#income_incomeId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (income, response, status) {
			$.messager.progress("close");
			if (income) { 
				$("#income_incomeId_modify").val(income.incomeId);
				$("#income_incomeId_modify").validatebox({
					required : true,
					missingMessage : "请输入收入id",
					editable: false
				});
				$("#income_incomeTypeObj_typeId_modify").combobox({
					url:"/IncomeType/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"typeId",
					textField:"typeName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#income_incomeTypeObj_typeId_modify").combobox("select", income.incomeTypeObjPri);
						//var data = $("#income_incomeTypeObj_typeId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#income_incomeTypeObj_typeId_edit").combobox("select", data[0].typeId);
						//}
					}
				});
				$("#income_incomeFrom_modify").val(income.incomeFrom);
				$("#income_incomeFrom_modify").validatebox({
					required : true,
					missingMessage : "请输入收入来源",
				});
				$("#income_payWayObj_payWayId_modify").combobox({
					url:"/PayWay/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"payWayId",
					textField:"payWayName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#income_payWayObj_payWayId_modify").combobox("select", income.payWayObjPri);
						//var data = $("#income_payWayObj_payWayId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#income_payWayObj_payWayId_edit").combobox("select", data[0].payWayId);
						//}
					}
				});
				$("#income_payAccount_modify").val(income.payAccount);
				$("#income_payAccount_modify").validatebox({
					required : true,
					missingMessage : "请输入支付账号",
				});
				$("#income_incomeMoney_modify").val(income.incomeMoney);
				$("#income_incomeMoney_modify").validatebox({
					required : true,
					validType : "number",
					missingMessage : "请输入收入金额",
					invalidMessage : "收入金额输入不对",
				});
				$("#income_incomeDate_modify").datebox({
					value: income.incomeDate,
					required: true,
					showSeconds: true,
				});
				$("#income_userObj_user_name_modify").combobox({
					url:"/UserInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"user_name",
					textField:"name",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#income_userObj_user_name_modify").combobox("select", income.userObjPri);
						//var data = $("#income_userObj_user_name_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#income_userObj_user_name_edit").combobox("select", data[0].user_name);
						//}
					}
				});
				$("#income_incomeMemo_modify").val(income.incomeMemo);
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#incomeModifyButton").click(function(){ 
		if ($("#incomeModifyForm").form("validate")) {
			$("#incomeModifyForm").form({
			    url:"Income/update/" + $("#income_incomeId_modify").val(),
			    onSubmit: function(){
					if($("#incomeEditForm").form("validate"))  {
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
			$("#incomeModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
