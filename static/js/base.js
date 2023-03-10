const timeFrames = ["00:00", "00:15", "00:30", "00:45", "01:00", "01:15", "01:30", "01:45", "02:00", "02:15", "02:30", "02:45", "03:00", "03:15", "03:30", "03:45", "04:00", "04:15", "04:30", "04:45", "05:00", "05:15", "05:30", "05:45", "06:00", "06:15", "06:30", "06:45", "07:00", "07:15", "07:30", "07:45", "08:00", "08:15", "08:30", "08:45", "09:00", "09:15", "09:30", "09:45", "10:00", "10:15", "10:30", "10:45", "11:00", "11:15", "11:30", "11:45", "12:00", "12:15", "12:30", "12:45", "13:00", "13:15", "13:30", "13:45", "14:00", "14:15", "14:30", "14:45", "15:00", "15:15", "15:30", "15:45", "16:00", "16:15", "16:30", "16:45", "17:00", "17:15", "17:30", "17:45", "18:00", "18:15", "18:30", "18:45", "19:00", "19:15", "19:30", "19:45", "20:00", "20:15", "20:30", "20:45", "21:00", "21:15", "21:30", "21:45", "22:00", "22:15", "22:30", "22:45", "23:00", "23:15", "23:30", "23:45", "24:00"];
$(document).ready(function(){
    $('#customChart').click(function(){
        if($(this).hasClass('active')){
            $(this).removeClass('active');
        }
        else{
            $(this).addClass('active');
            var otherTabs = document.getElementsByClassName("chartTab");
            for(var i = 0; i<otherTabs.length; i++){
                $(otherTabs[i]).removeClass('active');
            }
        }
        
        document.getElementById('chartdiv').style.display = '';
        document.getElementById('chartdiv-live').style.display = 'none';
    });
    $('.chartTab').click(function(){
        if($('#chart-custom').hasClass('show')){
            $('#customChart').click();
        }
        if($(this).attr('id')=='liveTab'){
            document.getElementById('chartdiv').style.display = 'none';
            document.getElementById('chartdiv-live').style.display = '';
        }
        else{
            document.getElementById('chartdiv').style.display = '';
            document.getElementById('chartdiv-live').style.display = 'none';
        }
    });

    $('[data-toggle="popover"]').popover();   
    $("#popover").popover({ trigger: "hover focus" });

    /*var timeControllers = document.getElementsByClassName('time-control');
    for(var i = 0; i<timeControllers.length; i++){
        var currTimeController = timeControllers[i];
        for(var j = 0; j<timeFrames.length; j++){
            currTimeController.innerHTML += '<option>'+ timeFrames[j] +'</option>';
        }
    }*/
})

function formatPhoneNumber(x){
    return "("+ String(x).substring(0,3) + ") " + String(x).substring(3,6) + "-" + String(x).substring(6);
}

function formatDate(x){
    var startDate = new Date(x);
    var year = startDate.getFullYear();
    var month = addZero(startDate.getMonth()+1)
    var day = addZero(startDate.getDate())
    return year + '-' + month + '-' + day;
}

function formatNiceDate(x){
    var startDate = new Date(x);
    var year = startDate.getFullYear();
    var month = addZero(startDate.getMonth()+1)
    var day = addZero(startDate.getDate())
    return month + '/' + day + '/' + year;
}

function formatDateTime(x){
    var startDate = new Date(x);
    var year = startDate.getFullYear();
    var month = addZero(startDate.getMonth()+1)
    var day = addZero(startDate.getDate())

    var hours = startDate.getHours();
    var minutes = addZero(startDate.getMinutes())
    return year + '-' + month + '-' + day + ' ' + hours + ':' + minutes;
}

function formatNiceDateTime(x){
    if(x == null){
        return '-';
    }
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    var startDate = new Date(x);
    var year = startDate.getFullYear();
    var month = months[startDate.getMonth()]
    var day = addZero(startDate.getDate())

    var hours = startDate.getHours() > 12?addZero(startDate.getHours()-12):addZero(startDate.getHours());
    var minutes = addZero(startDate.getMinutes())

    var amPM = startDate.getHours() < 12 ? 'AM':'PM'; 
    return day + ' ' + month + ', ' + year + ' ' + hours + ':' + minutes + amPM;
}

function getDifference(first, last){
    return first-last;
}

function addZero(x){
    var strReturn = String(x);
    if(x < 10){
        strReturn = '0'+strReturn;
    }
    return strReturn;
}

function removeString(str, strRemove, replace=''){
    var newStr = str.split(strRemove).join(replace);
    return newStr;
}

function returnDash(str){
    if(str && str != ''){
        return str;
    }
    return '-';
}

function formatMoney(amount, decimalCount = 2, decimal = ".", thousands = ",") {
    try {
        decimalCount = Math.abs(decimalCount);
        decimalCount = isNaN(decimalCount) ? 2 : decimalCount;

        const negativeSign = amount < 0 ? "-" : "";

        let i = parseInt(amount = Math.abs(Number(amount) || 0).toFixed(decimalCount)).toString();
        let j = (i.length > 3) ? i.length % 3 : 0;

        return negativeSign + (j ? i.substr(0, j) + thousands : '') + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + thousands) + (decimalCount ? decimal + Math.abs(amount - i).toFixed(decimalCount).slice(2) : "");
    } catch (e) {
        //console.log(e)
    }
}

$('body').on('click','.copy-btn', function(){
    var id = $(this).attr('data-target');
    var copy_id = id+"-copied";
    var copy_text = document.getElementById(copy_id);
    $(copy_text).show();
    $(copy_text).hide();
    $(copy_text).fadeIn(200);

    /* Get the text field */
    var copyText = document.getElementById(id);
  
    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /* For mobile devices */
  
    /* Copy the text inside the text field */
    navigator.clipboard.writeText(copyText.value);

    setTimeout(function(){
        $(copy_text).fadeOut(200);
    },2000);
});

var functions = {
    updateCompanies: function(){
        location.reload();
        updateCompanies()
    },
    updateForms: function(){updateForms()},
    updateCurrentForm: function(){updateForms(); updateCurrentForm()},
    updateCampaigns: function(){updateCampaigns()},
    updateCallCampaigns: function(){updateCallCampaigns()},
    reloadPage: function(){
        document.getElementById("lead-import-loading").style.display = 'none';
        document.getElementById("lead-import-card").style.display = '';
        location.reload();
    },
    updateWalletBalance: function(){
        $('#company-body').change();
    },
    updateRoles:function(){updateRoles()},
    updateusers:function(){updateusers()},
    updateTwilio:function(){
        updateTwilio()
    },
    updateEmailSettings:function(){updateEmailSettings()},
    updatePaymentSettings:function(){updatePaymentSettings()},
    updateCallerIDs:function(){updateCallerIDs()},
    updateVirtualAgentsAdmin:function(){updateVirtualAgentsAdmin()},
    updateLists:function(){updateLists()},
    getCallerIDGroups:function(){$("#caller-id-group-body").change();},
    doneImporting:function(){doneImporting();},
    doNothing:function(){$(".sidebar-transparent").click();}
}

function postToAPI(url, payload, type = "POST", returnFunction){
    document.getElementById("alert-holder").style.display = '';
    $.ajax({
        type: type,
        url: url,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify(payload),
        success: function(data){
            console.log("data");
            console.log(data);
            if(data['Message'] == 'Success'){
                alerts.alerts.push({
                    "status":"success",
                    "message":"Update was successful"
                })
                if(returnFunction){
                    setTimeout(function(){
                        functions[returnFunction]();
                    }, 1000)
                }
            }
            else{
                alerts.alerts.push({
                    "status":"danger",
                    "message":"Failed to save"
                })
                if(returnFunction){
                    setTimeout(function(){
                        functions[returnFunction]();
                    }, 1000)
                }
            }
        },
        error: function(data){
            console.log('FAILURE');
        }
    });
}

function setLocationUrl(id){
    return '/leads?campaign_id='+id;
}

function calculateProgressBars(){
    var campaigns = document.getElementsByClassName('progress-bar');
    for(var i = 0; i<campaigns.length; i++){
        var startValue = $(campaigns[i]).attr('aria-valuenow');
        var maxValue = $(campaigns[i]).attr('aria-valuemax');
        var newWidth = String((parseFloat(startValue)/parseFloat(maxValue)) * 100) + '%';
        campaigns[i].style.width = newWidth;
    }
}

function validateForm(ids){
    var valid = true;
    for(var i = 0; i<ids.length; i++){
        var domValue = $(ids[i]).val();
        if(domValue == '' || domValue === undefined){
            valid = false;
            $(ids[i]).addClass('border'); 
            $(ids[i]).addClass('border-danger');
            
            var warningID = ids[i].substring(1) + '-' + 'warning';
            var html = '<span id="'+warningID+'" class="text-danger">Cannot be blank</span>';
            $(ids[i]).parent().append(html);
        }
        else{
            $(ids[i]).removeClass('border'); 
            $(ids[i]).removeClass('border-danger'); 
            var warningID = ids[i].substring(1) + '-' + 'warning';
            try{
                document.getElementById(warningID).remove();
            }catch(error){}
        }
    }
}

function getTimeFormat(x){
    var hours = x/3600;
    var minutes = (hours%1)*60;
    var seconds = (minutes%1)*60;

    return String(parseInt(hours)) + 'H ' +  String(parseInt(minutes)) + 'M ' +  String(parseInt(seconds)) + 'S';
}
const dispoDescriptions = {
    "AA":"Answering Machine",
    "AB":"Busy",
    "ADC":"Disconnected Number",
    "DROP":"Agent Unavailable",
    "LRERR":"Local Dial Error",
    "NA":"No Answer",
    "PDROP":"Outbound Pre-Routing Drop",
    "XFER":"Call Transferred"
}
function dispoDescriptor(dispo){
    return dispoDescriptions[dispo];
}

var alerts = new Vue({
    delimiters: ['[[', ']]'],
    el: '#alert-holder',
    data: {
        alerts:[]
    }
})

$('body').on('click','.form-control', function(){
    resetMinMax(this);
})

$('body').on('change','.form-control', function(){
    resetMinMax(this);
})

$('body').on('keydown','.form-control', function(){
    resetMinMax(this);
})

function resetMinMax(x){
    var min = $(x).attr('min');
    var max = $(x).attr('max');
    var value = $(x).val();

    if(min && min !== undefined){
        if(!isNaN(parseFloat(min))){
            if(!isNaN(parseFloat(value))){
                if(parseFloat(min)>parseFloat(value)){
                    $(x).val(parseFloat(min));
                }
            }
        }
    }

    if(max && max !== undefined){
        if(!isNaN(parseFloat(max))){
            if(!isNaN(parseFloat(value))){
                if(parseFloat(max)<parseFloat(value)){
                    $(x).val(parseFloat(max));
                }
            }
        }
    }
}