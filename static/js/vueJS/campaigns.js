try{
    document.getElementById('campaign-body-loading').style.display = '';
    document.getElementById('campaign-body').style.display = 'none';
}catch(error){}
try{
    document.getElementById('campaign-edit-loading').style.display = '';
    document.getElementById('campaign-edit-body').style.display = 'none';
}catch(error){}

var campaignID;
var campaigns = new Vue({
    delimiters: ['[[', ']]'],
    el: '#campaign-body',
    data: {
        campaigns:[]
    }
})

var campaignDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#campaign-edit',
    data: {
        details:{},
        virtualAgents:[]
    }
})

function updateCampaigns(){
    $(".sidebar-transparent").click();
    try{
        document.getElementById('campaign-body-loading').style.display = '';
        document.getElementById('campaign-body').style.display = 'none';
    }catch(error){}
    var jqxhr = $.get( '/api/v1/campaigns?limit=2000', function(data) {
        console.log(data);
        campaigns.campaigns = data;
        try{
            document.getElementById('campaign-body-loading').style.display = 'none';
            document.getElementById('campaign-body').style.display = '';
        }catch(error){}
    }).always(function(){
        try{
            document.getElementById('campaign-body-loading').style.display = 'none';
            document.getElementById('campaign-body').style.display = '';
        }catch(error){}
        setTimeout(function(){
            calculateProgressBars();
            updateNotification();
        },1000);
    });
    var jqxhr = $.get( '/api/v1/virtual-agents?limit=2000', function(data) {
        campaignDetails.virtualAgents = data;
    });
}

$('#add-company').click(function(){
    postData = {
        "name":$('#addCampaignName').val(),
        "status":'stopped',
        "started_on":null,
        "total_leads":0,
        "remaining_leads":0,
        "auto_reference":document.getElementById('addCampaignARE').checked ? 1:0,
        "form_id":$('#addCampaignForm').val(),
        "auto_reference_prefix":$('#addCampaignARP').val(),
        "user_data":[]
    }
    var campaignAddUsers = document.getElementsByClassName('campaignAddUser');
    for(var i = 0; i<campaignAddUsers.length; i++){
        postData['user_data'].push({
            'user_id':$(campaignAddUsers[i]).attr('user-id')
        })
    }
    console.log(postData);
    try{
        document.getElementById('campaign-body-loading').style.display = '';
        document.getElementById('campaign-body').style.display = 'none';
    }catch(error){}
    postToAPI('/api/v1/campaigns', postData, 'POST', 'updateCampaigns');
});
$('body').on('click','#edit-company', function(){
    try{
        document.getElementById('campaign-edit-loading').style.display = '';
        document.getElementById('campaign-edit-body').style.display = 'none';
    }catch(error){}
    var agentTypes = $('.agent-type');
    var agentType = $(agentTypes[0]).hasClass('active');
    var numAgents = 1;
    var callsPerAgent = 1;
    if(agentType){
        numAgents = 0;
        callsPerAgent = $('#total-calls').val();
    }
    else{
        numAgents = $('#num-agent').val();
        callsPerAgent = $('#calls-per-agent').val();
    }
    var postData = {
        'id':campaignID,
        'name':$('#campaignEditName').val(),
        'schedule_data':[],
        'num_agents':numAgents,
        'calls_per_agent':callsPerAgent,
        'did':$("#campaignEditDID").val()
    }
    var timers = $(".timer");
    var switches = $(".dayEnabled");
    for(var i = 0; i<timers.length; i++){
        var id = $(timers[i]).attr('day-value')+'Enabled';
        console.log(id);
        postData['schedule_data'].push({
            "day_value":$(timers[i]).attr('day-value'),
            "status":$(timers[i]).attr('day-status'),
            "time_full":convertTime($(timers[i]).val()),
            'enabled':document.getElementById(id).checked ? true:false
        })
    }
    console.log(postData)
    if($("#virtual-agent-body").val() != 'None'){
        postData['virtual_agent_id'] = $("#virtual-agent-body").val();
    }
    postToAPI('/api/v1/campaigns', postData, 'PUT', 'updateCampaigns');
});

$('body').on('click','.campaign-delete', function(){
    campaignID = $(this).attr('campaign-id');
    try{
        document.getElementById('campaign-body-loading').style.display = '';
        document.getElementById('campaign-body').style.display = 'none';
    }catch(error){}
    var postData = {
        'id':campaignID
    }
    try{
        document.getElementById('campaign-body-loading').style.display = '';
        document.getElementById('campaign-body').style.display = 'none';
    }catch(error){}
    postToAPI('/api/v1/campaigns', postData, 'DELETE', 'updateCampaigns');
});

$('body').on('click','.campaign-edit', function(){
    campaignID = $(this).attr('campaign-id');
    var url = '/api/v1/campaigns?campaignid='+campaignID;
    console.log(url);
    try{
        document.getElementById('campaign-edit-loading').style.display = '';
        document.getElementById('campaign-edit-body').style.display = 'none';
    }catch(error){}
    var jqxhr = $.get( url, function(data) {
        campaignDetails.details = data[0];
        console.log(campaignDetails);
        if(data[0]['num_agents'] == 0 && data[0]['calls_per_agent'] > 0){
            $("#tab1").click();
        }
        else{
            $("#tab2").click();
        }
    }).always(function(){
        setTimeout(function(){
            $('.datetimepicker').datetimepicker({
                icons: {
                    time: "fa fa-clock",
                    date: "fa fa-clock",
                    up: "fa fa-chevron-up",
                    down: "fa fa-chevron-down",
                    previous: 'fa fa-chevron-left',
                    next: 'fa fa-chevron-right',
                    today: 'fa fa-screenshot',
                    clear: 'fa fa-trash',
                    close: 'fa fa-remove'
                },
                format: 'LT'
            });
            try{
                document.getElementById('campaign-edit-loading').style.display = 'none';
                document.getElementById('campaign-edit-body').style.display = '';
            }catch(error){}
        }, 1000)
    })
});

updateCampaigns();

$('body').on('click','.lead-export', function(){
    var url = '/api/v1/leads/export?campaignid='+$(this).attr('campaign-id');
    var csv = '';
    var jqxhr = $.get( url, function(data) {
        data.forEach(function(row) {
            csv += row.join(',');
            csv += "\n";
        });
        console.log(csv);
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'leads.csv';
        hiddenElement.click();
    })
});

function convertTime(x){
    x = '2021-01-01 ' + x;
    var d = new Date(x);
    var hour = addZero(d.getHours());
    var minutes = addZero(d.getMinutes());
    return hour + ':' + minutes + ':00';
}

function convertNiceTime(x){
    x = '2021-01-01 ' + x;
    var d = new Date(x);
    var hour = d.getHours() > 12 ? (d.getHours()-12): (d.getHours());
    var amPM = d.getHours() > 11 ? 'PM':'AM';
    var minutes = addZero(d.getMinutes());
    return hour + ':' + minutes + ' ' + amPM;
}

function getFlatCall(x,y){
    if(x == 0){
        x = 1;
    }
    return x*y;
}