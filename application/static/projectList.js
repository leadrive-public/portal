var pjList=Vue.component("pj-list",{
    props:['list','user'],
    data:function(){
        return {
            projects:null,
            users:null,
            showOpenProjects:true,
            showClosedProjects:false,
            showAllProjects:false,
            filterStr:"",
            ajaxStatus:"",
            showPmCol:false,
            showSeCol:false,
            showStatusCol:true,
            showStageCol:true,
            showProgressCol:true,
            showActivityCol:true,
        };
    },
    template:`
    <div>
        <div class="btn-group mr-1">
            <button class="btn btn-outline-secondary" title="Show all tasks" @click="showAllProjectsClickHandler" :class="{'active': (showOpenProjects && showClosedProjects)}">
                <span style="width:1.18rem;display:inline-block">All</span>
            </button>
            <button class="btn btn-outline-secondary" title="Show open tasks" @click="showOpenProjectsClickHandler" :class="{'active': (showOpenProjects && !showClosedProjects)}">
                <span style="width:1.18rem;display:inline-block">O</span>
            </button>
            <button class="btn btn-outline-secondary" title="Show closed tasks" @click="showClosedProjectsClickHandler" :class="{'active': (!showOpenProjects && showClosedProjects)}">
                <span style="width:1.18rem;display:inline-block">C</span>
            </button>
        </div>
        <div class="btn-group mr-1">
            <button class="btn btn-outline-secondary" title="Show PM column" @click="showPmCol=!showPmCol;" :class="{'active': (showPmCol)}">
                PM
            </button>
            <button class="btn btn-outline-secondary" title="Show SE column" @click="showSeCol=!showSeCol;" :class="{'active': (showSeCol)}">
                SE
            </button>
            <button class="btn btn-outline-secondary" title="Show status column" @click="showStatusCol=!showStatusCol;" :class="{'active': (showStatusCol)}">
                Status
            </button>
            <button class="btn btn-outline-secondary" title="Show stage column" @click="showStageCol=!showStageCol;" :class="{'active': (showStageCol)}">
                Stage
            </button>
            <button class="btn btn-outline-secondary" title="Show progress column" @click="showProgressCol=!showProgressCol;" :class="{'active': (showProgressCol)}">
                Progress
            </button>
            <button class="btn btn-outline-secondary" title="Show activity column" @click="showActivityCol=!showActivityCol;" :class="{'active': (showActivityCol)}">
                Activity
            </button>
        </div>
        <table class="table table-hover table-sm" >
            <thead>
                <tr>
                    <th class="pj-pjCell">Project</th>
                    <th class="pj-titleCell">Title</th>
                    <th class="pj-pmCell" :class="{'d-none': !showPmCol}">PM</th>
                    <th class="pj-seCell" :class="{'d-none': !showSeCol}">SE</th>
                    <th class="pj-statusCell" :class="{'d-none': !showStatusCol}">Status</th>
                    <th class="pj-stageCell" :class="{'d-none': !showStageCol}">Stage</th>
                    <th class="pj-progressCell" :class="{'d-none': !showProgressCol}">Progress</th>
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
                            <td class="pj-pmCell" :class="{'d-none': !showPmCol}">-</td>
                            <td class="pj-seCell" :class="{'d-none': !showSeCol}">-</td>
                            <td class="pj-statusCell" :class="{'d-none': !showStatusCol}" v-html="getStatusValue(project)"></td>
                            <td class="pj-stageCell" :class="{'d-none': !showStageCol}">{{getStageValue(project)}}</td>
                            <td class="pj-progressCell" :class="{'d-none': !showProgressCol}">-</td>
                            <td class="pj-activityCell" :class="{'d-none': !showActivityCol}">-</td>
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
        getProject_beforeCallback:function(){
            this.ajaxStatus="running";
        },
        getProject_successCallback:function(rsp){
            this.ajaxStatus="success";
            console.log(rsp);
            this.projects=rsp.projects;
            this.users=rsp.users;
        },
        getProject_errorCallback:function(){
            this.ajaxStatus="error";
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
        }
    },
    mounted:function(){
        let req =
        {
            function: "getProjects",
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
    },
});


