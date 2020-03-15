var comment=Vue.component("ioi-comment",{
    props:["user", "editTime", "content"],
    data:function(){
        return {
            userName:"",
        };
    },
    template:`
    <div class="border rounded border-secondary p-2">
        <div class="d-flex">
            <div class="d-inline font-weight-bold">{{userDisplayName}}</div>
            <span style="width: 1em"></span>
            <div class="align-self-end small">{{editTime}}</div>
        </div>
        <br />
        <div class="text-wrap text-break" style="white-space: pre-line !important;">{{content}}</div>
    </div>
    `,
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
var taskList=Vue.component("ioi-edit",{
    props:['code','task'],
    data:function(){
        return {
            weekDate:new Date(),
            ajaxStatus:"",
            update:null,
            latestUpdates:[]
        };
    },
    template:`
    <div>
        <div class="alert alert-info" role="alert" v-if="ajaxStatus=='running'">
            <div class="spinner-border spinner-border-sm text-info" role="status">
                <span class="sr-only">Loading...</span>
            </div>
            Fetching data from the server...
        </div>
        <div class="alert alert-danger" role="alert" v-if="ajaxStatus=='error'">
            Fail to get data from the server!
        </div>
        <div v-if="ajaxStatus=='success'">
            <p>W{{DateTime.getWeekNumber(weekDate)}}: {{DateTime.getDateString(DateTime.getFirstDayOfWeek(weekDate))}} to {{DateTime.getDateString(DateTime.getLastDayOfWeek(weekDate))}}</p>
            <div class="form-row m-0">
                <label class="col-sm-2 pl-0">Project:</label>
                <label class="col-sm-10">{{code}}</label>
            </div>
            <div class="form-row m-0">
                <label class="col-sm-2 pl-0">Task:</label>
                <label class="col-sm-10">{{getTaskDisplayValue(update)}}</label>
            </div>
            <div class="form-row m-0">
                <label class="col-sm-2 pl-0">Hours:</label>
                <label class="col-sm-10">0</label>
            </div>
            <div class="d-flex justify-content-between mb-1">
                <label>Updates of this week:</label>
                <button class="btn btn-primary btn-sm">Save</button>
            </div>
            <div class="form-group">
                <textarea class="form-control border border-primary p-2" rows="4" v-model="update.content"></textarea>
            </div>
            <hr />
            <div v-if="!showLatestUpdates">There is not other updates.</div>
            <div v-if="showLatestUpdates">
                <div class="d-flex justify-content-between mb-1">
                    <label>Latest updates and comments:</label>
                    <button class="btn btn-secondary btn-sm">View history</button>
                </div>
                <div v-for="latestUpdate in latestUpdates">
                    <ioi-comment :user="latestUpdate.user" :content="latestUpdate.content" :editTime="latestUpdate.editTime"></ioi-comment>
                </div>
            </div>
        </div>

    </div>
    `,
    computed:{
        weekNumber:function(){
            return 0;
        },
        showLatestUpdates:function(){
            if (this.latestUpdates===null || this.latestUpdates ===undefined ) return false;
            if (this.latestUpdates.length===0) return false;
            return true;
        }
    },
    methods:{
        getTaskDisplayValue:function(task){
            if (task.task===0) return "0:非特定任务";
            else return task.task+":"+task.title;
        },
        getData_beforeCallback:function(){
            this.ajaxStatus="running";
        },
        getData_successCallback:function(rsp){
            console.info(`${new Date().toJSON()}: Success to get data from the server!`);
            console.log(rsp);
            if (rsp.isSuccess){
                this.ajaxStatus="success";
                this.update=rsp.update;
                this.latestUpdates=rsp.latestUpdates;
                this.weekDate=new Date(rsp.weekDate);
            }
            else{
                this.ajaxStatus="error";
                this.tasks=null;
                console.warn(rsp.exceptionMessage);
            }
        },
        getData_errorCallback:function(){
            console.error(`${new Date().toJSON()}: Fail to fetch data from the server!`);
            this.tasks=null;
            this.ajaxStatus="error";
        }
    },
    mounted:function(){
        $.ajax({
            type: "POST",
            url: "/ioi/service",
            contentType: "application/json",
            data: JSON.stringify({
                function:"getUpdate",
                code:this.code,
                task:this.task,
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

});