// JavaScript Document
+(function($){
	//Plugin For Pic
	//============================
	var Pic=function(){
		$(".pic").mouseenter(function(){
			//$(this).css("background","#000");
		});	

	}
	
	//regeister Plugin
	//===========================
	$(window).on('load',function(){
		Pic();
		$(".btt").hide();
	});
	$(window).scroll(function(){
		if($(window).scrollTop()>500){
			$(".btt").show();	
		}
		else{
			$(".btt").hide();
		}
	});
})(jQuery);