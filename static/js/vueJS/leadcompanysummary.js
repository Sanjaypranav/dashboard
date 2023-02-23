try{
    document.getElementById('company-lead-summary-loading').style.display = '';
    document.getElementById('company-lead-summary').style.display = 'none';
}catch(error){}
var campaignid; 
var companyLeadSummary = new Vue({
    delimiters: ['[[', ']]'],
    el: '#company-lead-summary',
    data: {
        summary:{}
    }
})

function updateCompanyLeadSummary(){
    try{
        document.getElementById('company-lead-summary-loading').style.display = '';
        document.getElementById('company-lead-summary').style.display = 'none';
    }catch(error){}
    var url = '/api/v1/lead/campaign-summary';
    if(campaignid){
        url = '/api/v1/lead/campaign-summary?campaignid='+campaignid;
    }
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        companyLeadSummary.summary = data;
        try{
            document.getElementById('company-lead-summary-loading').style.display = 'none';
            document.getElementById('company-lead-summary').style.display = '';
        }catch(error){}
    });
}

$('body').on('change','.lead-campaigns', function(){
    console.log('Testing')
    campaignid = $(this).val();
    updateCompanyLeadSummary();
});