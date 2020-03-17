function siteMaster_getQueryString(name) {
    let result = decodeURIComponent(location.search).toLowerCase().match(new RegExp("[\?\&]" + name.toLowerCase() + "=([^\&]+)", "i"));
    if (result === null || result.length < 1) {
        return "";
    }
    return result[1];
}
function siteMaster_htmlCoding(str)
{
    try
    {
        var s = String(str);
        s = s.replace(/&/g, '&amp;');
        s = s.replace(/</g, '&lt;');
        s = s.replace(/>/g, '&gt;');
        s = s.replace(/"/g, '&quot;');
        s = s.replace(/'/g, '&#039;');
        return s;
    }
    catch (err) { return ""; }
}
function siteMaster_renderTable(container, data, setting)
{
    let $container = $(container);
    $container.html("");
    $container.append("<table class='table table-hover table-sm'>"); let $table = $container.find("table");
    if ('responsive' in setting)
    {
        if (setting.responsive)
        {
            $container.css("display", "block");
            $container.css("width", "100%");
            $container.css("overflow-x", "auto");
            $container.addClass("table-responsive")
            $table.css("table-layout", "fixed");
        }
    }    let $thead, $tr, $td, $tbody, $tfoot;
    // thead
    $table.append("<thead>"); $thead = $table.find("thead");
    $thead.append("<tr>"); $tr = $thead.find("tr");
    for (let i = 0; i < setting.fields.length; i++)
    {
        $tr.append("<th>"); $td = $tr.find("th").last();
        if ("title" in setting.fields[i]) { $td.html(setting.fields[i].title); } else { $td.html(setting.fields[i].name); }
        if ("style" in setting.fields[i]) { $td.attr("style", setting.fields[i].style); } 
    }
    // tbody
    $table.append("<tbody>"); $tbody = $table.find("tbody");
    for (let i = 0; i < data.length; i++)
    {
        $tbody.append("<tr>"); $tr = $tbody.find("tr").last();
        let item = data[i];
        for (var j = 0; j < setting.fields.length; j++)
        {
            $tr.append("<td>"); $td = $tr.find("td").last();
            if ("template" in setting.fields[j])
            {
                var template = setting.fields[j].template;
                $td.html(template(item));
            }
            else
            {
                var fieldValue = eval("item." + setting.fields[j].name);
                $td.html(siteMaster_htmlCoding(fieldValue));
            }
            if ("style" in setting.fields[j]) { $td.attr("style", setting.fields[j].style); } 
        }
    }
}
function sitemaster_getUuid() {
    var d = new Date().getTime();
    if (window.performance && typeof window.performance.now === "function") {
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
}
var sitemaster_linkitem=Vue.component("sitemaster-link-item",{
    props:['linkitem'],
    template:`
    <div class="col sitemaster-link-item">
        <a :href="linkitem.link">
            <h4 class1="font-weight-bold">{{linkitem.title}}</h4>
            <p>{{linkitem.description}}</p>
        </a>
    </div>
    `,

});
var sitemaster_linkgroup=Vue.component("sitemaster-link-group",{
    props:['linkitems'],
    template:`
    <div class="row row-cols-1 row-cols-md-2 row-cols-xl-3">
        <sitemaster-link-item v-for="linkitem in linkitems" :linkitem="linkitem"></sitemaster-link-item>
    </div>
    `,
});

var siteMaster_userNameLabel=Vue.component("sm-username-label",{
    props:["user"],
    data:function(){
        return {
            userName:"",
        };
    },
    template:`<span>{{userDisplayName}}</span>`,
    computed:{
        userDisplayName:function(){
            if (this.userName!==""){return this.userName;}
            else{return this.user;}
        },
    },
    watch:{
        user:function(){
            this.getUserName();
        }
    },
    methods:{
        getData_beforeCallback:function(){
            this.userName="";
        },
        getData_successCallback:function(rsp){
            if (rsp.isSuccess){this.userName=rsp.displayName;}
            else{this.userName="";}
        },
        getData_errorCallback:function(){
            this.userName="";
        },
        getUserName:function(){
            $.ajax({
                type: "POST",
                url: "/user/service",
                contentType: "application/json",
                data: JSON.stringify({
                    function:"getUser",
                    id:this.user,
                }),
                dataType: "json",
                async: true,
                context: this,
                beforeSend: this.getData_beforeCallback,
                success: this.getData_successCallback,
                error: this.getData_errorCallback,
                complete: null,
            });
        },
    },
    mounted:function(){
        this.getUserName();
    }
});