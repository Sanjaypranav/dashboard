function _0x15ca(){var a=[".control-campaign","updateCallCampaigns","get","Update Call Campaigns","fields","496oTXPbz","lead-form-details","1221735cwBsty","12953060qHoBkZ","form-name","push","lead_data","campaigns","/api/v1/campaigns/make-call","always","length","100180UFxKKr","#call-manager-body","288084mOaFiw","/api/v1/campaigns?campaignid=","#call-lead","log","body","campaign-id","val","/api/v1/campaigns","form-id","fullDetails","6QYgBnE","lead-form-details-loading","#reference_number","call-manager-body-loading","146790xvsITG","649DVxeez","attr","call-manager-body","7319060xUBYdL","2698Aveetq","display","73RaEINy","click","style","lead-call-data","details","105RRLoxx","none","getElementById","/api/v1/forms?formid="];return(_0x15ca=function(){return a})()}var _0x58439a=_0x2fd9;!function(){for(var a=_0x2fd9,e=_0x15ca();;)try{if(866978==-parseInt(a(243))*(parseInt(a(241))/2)+parseInt(a(248))/3*(parseInt(a(220))/4)+-parseInt(a(211))/5*(-parseInt(a(232))/6)+-parseInt(a(240))/7+parseInt(a(257))/8*(parseInt(a(236))/9)+parseInt(a(212))/10+-parseInt(a(237))/11*(parseInt(a(222))/12))break;e.push(e.shift())}catch(a){e.push(e.shift())}}();try{document.getElementById(_0x58439a(235)).style[_0x58439a(242)]="",document[_0x58439a(250)](_0x58439a(239))[_0x58439a(245)][_0x58439a(242)]=_0x58439a(249)}catch(a){}calculateProgressBars();var callCampaigns=new Vue({delimiters:["[[","]]"],el:_0x58439a(221),data:{campaigns:[]}});function _0x2fd9(a,e){var t=_0x15ca();return(_0x2fd9=function(a,e){return t[a-=211]})(a,e)}function updateCallCampaigns(){var t=_0x58439a;console[t(225)](t(255)),callCampaigns.campaigns=[];try{document[t(250)](t(235)).style[t(242)]="",document[t(250)](t(239)).style[t(242)]=t(249)}catch(a){}$[t(254)]("/api/v1/campaigns?limit=2000",function(a){var e=t;console[e(225)](a),callCampaigns[e(216)]=a})[t(218)](function(){var a=t;try{document.getElementById(a(235))[a(245)][a(242)]=a(249),document.getElementById(a(239))[a(245)][a(242)]=""}catch(a){}setTimeout(function(){calculateProgressBars()},1e3)})}$(_0x58439a(226)).on(_0x58439a(244),_0x58439a(252),function(){var a=_0x58439a,e={status:$(this)[a(238)]("campaign-status"),id:$(this)[a(238)](a(227))};console[a(225)](e),postToAPI(a(229),e,"PUT",a(253))});var campaignID,leadFormDetails=new Vue({delimiters:["[[","]]"],el:"#lead-form-details",data:{details:[]}});$(_0x58439a(226)).on("click",".campaign-call",function(){var e=_0x58439a;campaignID=$(this)[e(238)]("campaign-id"),csvDetails[e(256)]=[],csvDetails[e(231)]=[],document.getElementById(e(233))[e(245)][e(242)]="",document.getElementById(e(258))[e(245)].display=e(249);$[e(254)](e(223)+campaignID,function(a){var t=e,a=a[0].form_id,a=t(251)+a;$.get(a,function(a){var e=t;console[e(225)](a[0][e(256)]),leadFormDetails[e(247)]=a[0][e(256)],document[e(250)](e(233))[e(245)][e(242)]=e(249),document.getElementById(e(258))[e(245)][e(242)]=""})})}),$(_0x58439a(224))[_0x58439a(244)](function(){var a=_0x58439a,e=a(217);postData={reference_number:$(a(234))[a(228)](),campaign_id:campaignID,lead_data:[]};for(var t=document.getElementsByClassName(a(246)),n=0;n<t[a(219)];n++)postData[a(215)][a(214)]({field_name:$(t[n])[a(238)](a(213)),field_value:$(t[n]).val(),form_field_id:$(t[n])[a(238)](a(230))});console.log(postData),postToAPI(e,postData,"POST",a(253))});try{document[_0x58439a(250)]("call-manager-body-loading")[_0x58439a(245)][_0x58439a(242)]=_0x58439a(249),document[_0x58439a(250)](_0x58439a(239))[_0x58439a(245)][_0x58439a(242)]=""}catch(a){}