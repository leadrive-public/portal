var taskList=Vue.component("ioi-tasklist",{
    data:function(){
        return {
            weekDate:new Date(),
            ajaxStatus:"",
            tasks:[],
        };
    },
    template:`
    <div>
        <div class="alert alert-info" role="alert" v-if="ajaxStatus=='running'">
            <div class="spinner-border spinner-border-sm text-info" role="status">
                <span class="sr-only">Loading...</span>
            </div>
            Searching data from the server...
        </div>
        <div class="alert alert-danger" role="alert" v-if="ajaxStatus=='error'">
            Fail to get codes from the server!
        </div>
        <div v-if="ajaxStatus=='success'">
            <h4>W{{DateTime.getWeekNumber(weekDate)}}: {{DateTime.getDateString(DateTime.getFirstDayOfWeek(weekDate))}} to {{DateTime.getDateString(DateTime.getLastDayOfWeek(weekDate))}}</h4>
            <table class="table table-sm table-striped table-hover" style="table-layout:fixed">
                <thead>
                    <tr>
                        <th class="ioi-code-col">Project</th>
                        <th class="ioi-task-col">Task</th>
                        <th class="ioi-hours-col">Hours</th>
                        <th class="ioi-content-col">Content</th>
                        <th class="ioi-edit-col"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="task in tasks">
                        <td class="ioi-code-col">{{task.code}}</td>
                        <td class="ioi-task-col">{{getTaskDisplayValue(task)}}</td>
                        <td class="ioi-hours-col">{{task.hours}}</td>
                        <td class="ioi-content-col">{{task.content}}</td>
                        <td class="ioi-edit-col"><a class="btn btn-sm btn-secondary" :href="'edit?code='+task.code+'&task='+task.task">Edit</a></td>
                    </tr>
                </tbody>
            </table>
        </div>

    </div>
    `,
    computed:{
        weekNumber:function(){
            return 0;
        },
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
                this.tasks=rsp.tasks;
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
            url: "service",
            contentType: "application/json",
            data: JSON.stringify({
                function:"getTasks",
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