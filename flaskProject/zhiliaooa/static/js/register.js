function bindEmailCaptchaClick(){
    $("#captcha-btn").click(function (event){
    //$this 代表的是当前按钮的jquery对象
     var $this = $(this);
     event.preventDefault();

     var email = $("input[name='email']").val();
     $.ajax({
        url : "/auth/captcha/email?email=" + email,
        method: "GET",
        success: function (result){
            var code = result['code'];
            if(code== 200){
                //加入倒计时功能
                var countdown =5;
                //开始倒计时之前，取消按钮的点击事件
                $this.off("click");
                var timer = setInterval(function (){
                    $this.text(countdown);
                    countdown -=1;
                    //倒计时结束的时候执行
                    if (countdown <=0){
                        //清除定时器
                        clearInterval(timer);
                        //将按钮的文字改回来
                        $this.text("获取验证码");
                        //重新绑定点击事件
                        bindEmailCaptchaClick();
                    }
                }, 1000);
                alert("邮箱验证码发送成功！");
            }
            else{
                alert(result['message']);
            }
        },
        fail: function (error){
            console.log(error);
        }
     })
    });
}



// 整个网页都加载完毕后再执行
$(function (){
    bindEmailCaptchaClick();
});