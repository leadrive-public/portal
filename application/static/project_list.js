var pjList=Vue.component("pj-list",{
    props:['list','user'],
    data:function(){
        return {
            projects:null,
            users:null,
            statistics:null,
            activities:null,

            showOpenProjects:true,
            showClosedProjects:false,
            showAllProjects:false,
            filterStr:"",

            ajaxStatus:"",
            statisticsAjaxStatus:"",
            activitiesAjaxStatus:"",
            showPmCol:true,
            showSeCol:true,
            showStatusCol:true,
            showStageCol:true,
            showBudget:true,
            showSpending:true,
            showProgressCol:true,
            showActivityCol:true,
            showTasks:true,
        };
    },
    template:`
    <div class="pj-list">
        <div class="btn-group mr-1">
            <button class="btn btn-secondary" title="Show all tasks" @click="showAllProjectsClickHandler" :class="{'active':showAllProjects}">
                <span style="width:1.18rem;display:inline-block">All</span>
            </button>
            <button class="btn btn-secondary" title="Show open tasks" @click="showOpenProjectsClickHandler" :class="{'active':showOpenProjects}">
                <span style="width:1.18rem;display:inline-block">O</span>
            </button>
            <button class="btn btn-secondary" title="Show closed tasks" @click="showClosedProjectsClickHandler" :class="{'active':showClosedProjects}">
                <span style="width:1.18rem;display:inline-block">C</span>
            </button>
        </div>
        <div class="btn-group mr-1">
            <button class="btn btn-secondary" title="Show PM column" @click="showPmCol=!showPmCol;" :class="{'active': (showPmCol)}">
                PM
            </button>
            <button class="btn btn-secondary" title="Show SE column" @click="showSeCol=!showSeCol;" :class="{'active': (showSeCol)}">
                SE
            </button>
            <button class="btn btn-secondary" title="Show status column" @click="showStatusCol=!showStatusCol;" :class="{'active': (showStatusCol)}">
                Status
            </button>
            <button class="btn btn-secondary" title="Show stage column" @click="showStageCol=!showStageCol;" :class="{'active': (showStageCol)}">
                Stage
            </button>
        </div>
        <div class="btn-group mr-1">
            <button class="btn btn-secondary" title="Show budget column" @click="showBudget=!showBudget;" :class="{'active': (showBudget)}">
                Budget
            </button>
            <button class="btn btn-secondary" title="Show spending column" @click="showSpending=!showSpending;" :class="{'active': (showSpending)}">
                Spend
            </button>
            <button class="btn btn-secondary" title="Show progress column" @click="showProgressCol=!showProgressCol;" :class="{'active': (showProgressCol)}">
                Progress
            </button>

            <button class="btn btn-secondary" title="Show tasks column" @click="showTasks=!showTasks;" :class="{'active': (showTasks)}">
                Tasks
            </button>
            <button class="btn btn-secondary" title="Show activity column" @click="showActivityCol=!showActivityCol;" :class="{'active': (showActivityCol)}">
                Activity
            </button>
        </div>
        <table class="table table-hover table-sm pj-table" >
            <thead>
                <tr>
                    <th class="pj-pjCell">Project</th>
                    <th class="pj-titleCell">Title</th>
                    <th class="pj-pmCell" :class="{'d-none': !showPmCol}">PM</th>
                    <th class="pj-seCell" :class="{'d-none': !showSeCol}">SE</th>
                    <th class="pj-statusCell" :class="{'d-none': !showStatusCol}">Status</th>
                    <th class="pj-stageCell" :class="{'d-none': !showStageCol}">Stage</th>
                    <th class="pj-budgetCell" :class="{'d-none': !showBudget}">Budget</th>
                    <th class="pj-spendingCell" :class="{'d-none': !showSpending}">Spend</th>
                    <th class="pj-progressCell" :class="{'d-none': !showProgressCol}">Progress</th>
                    <th class="pj-taskCell" :class="{'d-none': !showTasks}">Tasks</th>
                    <th class="pj-activityCell" :class="{'d-none': !showActivityCol}">Activity</th>
                </tr>
            </thead>
            <tbody>
                <!-- alert -->
                <tr v-if="ajaxStatus=='running'">
                    <td colspan="8">
                        <div class="alert alert-info" role="alert">
                            <div class="spinner-grow spinner-grow-sm text-info" role="status">
                                <span class="sr-only">Loading...</span>
                            </div>
                            Searching data from the server...
                        </div>
                    </td>
                </tr>
                <tr v-if="ajaxStatus=='error'">
                    <td colspan="8">
                        <div class="alert alert-danger" role="alert">
                            Fail to get codes from the server!
                        </div>
                    </td>
                </tr>
                <!-- content -->
                <template v-if="ajaxStatus=='success'">
                    <template v-for="project in projects">
                        <tr :class="{'d-none': !isVisibleProject(project)}">
                            <td class="pj-pjCell"><a :href="''+project.code">{{project.code}}</a></td>
                            <td class="pj-titleCell">{{project.title}}</td>
                            <td class="pj-pmCell" :class="{'d-none': !showPmCol}">{{getPmName(project)}}</td>
                            <td class="pj-seCell" :class="{'d-none': !showSeCol}">{{getSeName(project)}}</td>
                            <td class="pj-statusCell" :class="{'d-none': !showStatusCol}" v-html="getStatusValue(project)"></td>
                            <td class="pj-stageCell" :class="{'d-none': !showStageCol}">{{getStageValue(project)}}</td>
                            <td class="pj-budgetCell" :class="{'d-none': !showBudget}" v-html="getBudgetDisplayValue(project)"></td>
                            <td class="pj-spendingCell" :class="{'d-none': !showSpending}" v-html="getSpendingDisplayValue(project)">Spending</td>
                            <td class="pj-progressCell" :class="{'d-none': !showProgressCol}" v-html="getProgressDisplayValue(project)">-</td>
                            <td class="pj-taskCell" :class="{'d-none': !showTasks}" v-html="getTaskLabel(project)"></td>
                            <td class="pj-activityCell" :class="{'d-none': !showActivityCol}">{{getActivity(project)}}</td>
                        </tr>
                    </template>

                <template>
            </tbody>
        </table>
    </div>
    `,
    methods:{
        isVisibleProject:function(project){
            if (this.showOpenProjects && this.isOpenProject(project)) return true;
            if (this.showClosedProjects && this.isClosedProject(project)) return true;
            if (this.showAllProjects) return true;
            return false;
        },
        isOpenProject:function(project){
            if (project.status === null) return false;
            if (project.status === "open") return true;
            return false;
        },
        isClosedProject:function(project){
            if (project.status === null) return false;
            if (project.status === "closed") return true;
            return false;
        },
        getStatusValue:function(project){
            if (project.status === null) return `<span class="badge badge-light">N/A</span>`;
            if (project.status==="open") return `<span class="badge badge-warning">open</span>`;
            if (project.status==="closed") return `<span class="badge badge-success">closed</span>`;
            return project.status;
        },
        getStageValue:function(project){
            if (project.stage === null) return "-";
            return project.stage;
        },
        getBudgetDisplayValue:function(project){
            if (project.budget === null) return "-";
            return project.budget;
        },
        getSpendingDisplayValue:function(project){
            if (this.statistics===null) return "-";
            let code="PJ-"+project.code;
            let statisticItem=this.statistics.find(function(item){
                return item.code===code;
            });
            if (statisticItem===undefined || statisticItem===null) return "-";
            project.statistics=statisticItem.hours/40;
            let weeks=Math.round(project.statistics*10)/10;
            if (weeks>0) return weeks;
            else return "-";
        },
        getActivity:function(project){
            if (this.activities===null) return "-";
            let code="PJ-"+project.code;
            let activity=this.activities.find(function(item){
                return item.code===code;
            });
            if (activity===undefined || activity===null) return "-";
            project.activity=activity.hours/40;
            let weeks=Math.round(project.activity*10)/10;
            if (weeks>0) return weeks;
            else return "-";
        },
        getProgressDisplayValue:function(project){
            try{
                let statistics=project.statistics;
                let budget=project.budget;
                let progress=statistics/budget;
                if (isNaN(progress)) return "-";
                if (!isFinite(progress)) return "-";
                return Math.round(progress*100)+"%";
            }
            catch(e){return "-";}
        },
        getUserName:function(userId){
            let user=this.users.find(function(item){
                return item.id==userId;
            })
            if (user===undefined || user===null) return "";
            return user.displayName;
        },
        getPmName:function(project){
            if (project===undefined || project===null) return "-";
            if (!('pm' in project)) return "-";
            if (project.pm===null) return "-";
            return this.getUserName(project.pm);
        },
        getSeName:function(project){
            if (project===undefined || project===null) return "-";
            if (!('se' in project)) return "-";
            if (project.se===null) return "-";
            return this.getUserName(project.se);
        },
        getProject_beforeCallback:function(){
            this.ajaxStatus="running";
        },
        getProject_successCallback:function(rsp){
            console.info(`${new Date().toJSON()}: Success to get projects data from the server!`);
            console.log(rsp);
            if (rsp.isSuccess){
                this.ajaxStatus="success";
                this.projects=rsp.projects;
            }
            else{
                this.ajaxStatus="error";
                this.projects=null;
                console.warn(rsp.exceptionMessage);
            }
        },
        getProject_errorCallback:function(){
            this.ajaxStatus="error";
            this.projects=null;
            console.error(`${new Date().toJSON()}: Fail to fetch projects data from the server!`);
        },
        showOpenProjectsClickHandler:function(){
            this.showOpenProjects=true;
            this.showClosedProjects=false;
            this.showAllProjects=false;
        },
        showAllProjectsClickHandler:function(){
            this.showOpenProjects=false;
            this.showClosedProjects=false;
            this.showAllProjects=true;
        },
        showClosedProjectsClickHandler:function(){
            this.showOpenProjects=false;
            this.showClosedProjects=true;
            this.showAllProjects=false;
        },
        getTaskLabel:function(project){
            if (project===null || project===undefined ) return "-";
            if (!('tasks' in project)) return "-";
            let tasks=project.tasks;
            let openTasks=0, closedTasks=0, otherTasks=0;
            for(let task of tasks.values()){
                if (!('status' in task)) {
                    otherTasks+=1;
                    continue;
                }
                if(task.status==="open"){
                    openTasks+=1;
                }
                else if(task.status==="closed"){
                    closedTasks+=1;
                }
                else{
                    otherTasks+=1;
                }
            }
            return `<span class="badge badge-light">${otherTasks}</span>/<span class="badge badge-warning">${openTasks}</span>/<span class="badge badge-success">${closedTasks}</span>`;
        },
        getStatistics_beforeCallback:function(){
            this.statisticsAjaxStatus="running";
        },
        getStatistics_successCallback:function(rsp){
            console.info(`${new Date().toJSON()}: Success to get statistics data from the server!`);
            console.log(rsp);
            if (rsp.isSuccess){
                this.statisticsAjaxStatus="success";
                this.statistics=rsp.statistics;
            }
            else{
                this.statisticsAjaxStatus="error";
                this.statistics=null;
                console.warn(rsp.exceptionMessage);
            }
        },
        getStatistics_errorCallback:function(){
            this.statisticsAjaxStatus="error";
            this.statistics=null;
            console.error(`${new Date().toJSON()}: Fail to fetch statistics data from the server!`);
        },
        getActivities_beforeCallback:function(){
            this.activitiesAjaxStatus="running";
        },
        getActivities_successCallback:function(rsp){
            console.info(`${new Date().toJSON()}: Success to get activities data from the server!`);
            console.log(rsp);
            if (rsp.isSuccess){
                this.activitiesAjaxStatus="success";
                this.activities=rsp.activities;
            }
            else{
                this.activitiesAjaxStatus="error";
                this.activities=null;
                console.warn(rsp.exceptionMessage);
            }
        },
        getActivities_errorCallback:function(){
            this.activitiesAjaxStatus="error";
            this.activities=null;
            console.error(`${new Date().toJSON()}: Fail to fetch activities data from the server!`);
        },
        getUsers_successCallback:function(rsp){
            console.info(`${new Date().toJSON()}: Success to get user data from the server!`);
            console.log(rsp);
            if (rsp.isSuccess){
                this.userAjaxStatus="success";
                this.users=rsp.users;
            }
            else{
                this.userAjaxStatus="error";
                this.users=null;
                console.warn(rsp.exceptionMessage);
            }
        },
        getUsers_errorCallback:function(){
            this.userAjaxStatus="error";
            this.users=null;
            console.error(`${new Date().toJSON()}: Fail to fetch user data from the server!`);
        },
        getUsers_beforeCallback:function(){
            this.userAjaxStatus="running";
        }
    },
    mounted:function(){
        let req =
        {
            function: "getProjectList",
        };
        let rsp = $.ajax(
            {
                type: "POST",
                url: "service",
                contentType: "application/json",
                data: JSON.stringify(req),
                dataType: "json",
                async: true,
                context: this,
                beforeSend: this.getProject_beforeCallback,
                success: this.getProject_successCallback,
                error: this.getProject_errorCallback,
                complete: null,
            }).responseJSON;
        req={
            function: "getStatisticsByCode"
        };
        $.ajax({
            type: "POST",
            url: "/etime/service",
            contentType: "application/json",
            data: JSON.stringify(req),
            dataType: "json",
            async: true,
            context: this,
            beforeSend: this.getStatistics_beforeCallback,
            success: this.getStatistics_successCallback,
            error: this.getStatistics_errorCallback,
            complete: null,
        });
        $.ajax({
            type: "POST",
            url: "/etime/service",
            contentType: "application/json",
            data: JSON.stringify({
                function: "getActivitiesByCode"
            }),
            dataType: "json",
            async: true,
            context: this,
            beforeSend: this.getActivities_beforeCallback,
            success: this.getActivities_successCallback,
            error: this.getActivities_errorCallback,
            complete: null,
        });
        $.ajax({
            type: "POST",
            url: "/user/service",
            contentType: "application/json",
            data: JSON.stringify({
                function: "getUsers"
            }),
            dataType: "json",
            async: true,
            context: this,
            beforeSend: this.getUsers_beforeCallback,
            success: this.getUsers_successCallback,
            error: this.getUsers_errorCallback,
            complete: null,
        });
    },
});


