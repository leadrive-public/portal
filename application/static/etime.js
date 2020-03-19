class Etime {
    static getDateComponent(date) {
        let newDate = new Date();
        newDate.setTime(date.getTime());
        newDate.setUTCHours(0); newDate.setUTCMinutes(0); newDate.setUTCSeconds(0); newDate.setUTCMilliseconds(0);
        return newDate;
    }
    static getFirstDayOfWeek() {
        let date;
        if (arguments.length == 1) { date = arguments[0]; } else { date = new Date(); }
        date = this.getDateComponent(date)
        let firstDate = new Date();
        switch (date.getUTCDay()) {
            case 0://sunday -6day
                firstDate.setTime(date.getTime() - 6 * 1000 * 60 * 60 * 24);
                break;
            case 1://-0 day
            case 2://-1 day
            case 3://-2 day
            case 4://-3 day
            case 5://-4 day
            case 6://-5 day
                firstDate.setTime(date.getTime() + (1 - date.getDay()) * 1000 * 60 * 60 * 24);
                break;
        }
        return firstDate;
    }
    static getLastDayOfWeek() {
        let date;
        if (arguments.length == 1) { date = arguments[0]; } else { date = new Date(); }
        date = this.getDateComponent(date);
        let lastDate = new Date();
        switch (date.getUTCDay()) {
            case 0://sunday
                lastDate.setTime(date.getTime());
                break;
            case 1:
            case 2:
            case 3:
            case 4:
            case 5:
            case 6:
                lastDate.setTime(date.getTime() + (7 - date.getDay()) * 1000 * 60 * 60 * 24);
                break;
        }
        return lastDate;
    }
    static getFirstDayOfYear() {
        if (arguments.length == 0) {
            let day = new Date();
            day.setUTCMonth(0); day.setUTCDate(1); day.setUTCHours(0); day.setUTCMinutes(0); day.setUTCSeconds(0); day.setUTCMilliseconds(0);
            return day;
        }
        else {
            let day = new Date();
            day.setTime(arguments[0].getTime());
            day.setUTCMonth(0); day.setUTCDate(1); day.setUTCHours(0); day.setUTCMinutes(0); day.setUTCSeconds(0); day.setUTCMilliseconds(0);
            return day;
        }
    }
    static getWeekNumber(date) {
        let day1 = this.getFirstDayOfYear(date);
        let day2 = new Date();//to be the last day of week
        switch (day1.getUTCDay()) {
            case 0://sunday
                day2.setTime(day1.getTime());
                break;
            case 1:
            case 2:
            case 3:
            case 4:
            case 5:
            case 6:
                day2.setTime(day1.getTime() + (7 - day1.getDay()) * 1000 * 60 * 60 * 24);
                break;
        }
        let wk = 1;
        while (true) {
            if (date < day2) { return wk; }
            else { wk += 1; day2.setTime(day2.getTime() + 7 * 24 * 60 * 60 * 1000); }
            if (wk >= 60) { break; }
        }
        return wk;
    }
    static getDateString(date) {
        let str=date.toJSON();
        return str.substring(0,10);
    }
}
Vue.component("et-hoursinput", {
    props: ["value"],
    data: function(){
        return {
            bgClass:""
        };
    },
    template: `
        <div class="et-hourInput input-group">
            <input class="form-control et-hoursinput" type="text"  :class="[bgClass]" :value="displayValue" @change="changeHandler" placeholder=""/>
        </div>
    `,
    computed: {
        displayValue: function () {
            if (this.value === 0) return "";
            return this.value;
        }
    },
    methods: {
        changeHandler: function (event) {
            let value = event.target.value;
            let hours = Number(value);
            if (isNaN(hours)) {
                this.bgClass = "bg-danger";
            }
            else {
                if (hours < 0 || hours > 8) {
                    this.bgClass = "bg-danger";
                }
                else {
                    this.bgClass = "";
                }
                hours = Math.round(hours / 0.5) * 0.5;
                value = hours.toString();
            }
            this.$emit('input', value);
        }
    }
});
Vue.component("et-codeinput",{
    props:["record"],
    template:`
        <div class="et-codeInput input-group">
            <input class="form-control" type="text" placeholder="Select code..." readonly="readonly" v-model="record.code" />
            <div class="input-group-append">
                <button class="btn btn-outline-secondary" @click="selectHandler"><i class="search icon"></i></button>
            </div>
        </div>
    `,
    methods: {
        selectHandler: function () {
            //console.log("codeinput selectHandler");
            this.$emit("select", {sender: this, record: this.record});
        },
    }
});
Vue.component("et-taskinput",{
    props:["record"],
    data:function(){
        return{

        };
    },
    template:`
        <div class="et-taskInput input-group">
            <input class="form-control" type="text" placeholder="Select task..." readonly="readonly" :value="taskDisplayTitle" />
            <div class="input-group-append">
                <button class="btn btn-outline-secondary" @click="selectHandler"><i class="search icon"></i></button>
            </div>
        </div>
    `,
    computed:{
        taskDisplayTitle:function(){
            if (this.record.task<0) {
                return "";
            }
            else if ('taskTitle' in this.record){
                return `${this.record.task}:${this.record.taskTitle}`;
            }
            else{
                return `${this.record.task}`;
            }
            
        }
    },
    watch:{

    },
    methods: {
        selectHandler: function () {
            //console.log("taskinput selectHandler");
            if (this.record.code==""){
                return;
            }
            this.$emit("select", {sender: this, record: this.record});
        },
    }
});
Vue.component("et-weekeditor", {
    props: ["editor", "week"],
    data: function () {
        return {
            test: [2],
            
        };
    },
    template: `
        <div>
            <table class="et-table">
                <thead>
                   <tr>
                        <td colspan="7" class="et-weekspan">WK{{week.weekNumber}}: {{Etime.getDateString(week.startDate)}} to  {{Etime.getDateString(week.endDate)}}</td>
                    </tr>
                   <tr class="center aligned">
                        <th class="et-codeHeader">Code</th>
                        <th class="et-taskHeader">Task</th>
                        <th class="et-hourHeader">Mon<br />{{Monday.getMonth() + 1}}/{{Monday.getDate()}}</th>
                        <th class="et-hourHeader">Tue<br /> {{Tuesday.getMonth() + 1}}/{{Tuesday.getDate()}}</th>
                        <th class="et-hourHeader">Wed<br /> {{Wednesday.getMonth() + 1}}/{{Wednesday.getDate()}}</th>
                        <th class="et-hourHeader">Thu<br /> {{Thusday.getMonth() + 1}}/{{Thusday.getDate()}}</th>
                        <th class="et-hourHeader">Fri<br /> {{Friday.getMonth() + 1}}/{{Friday.getDate()}}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="record in week.records">
                        <td class="et-codeCell"><et-codeinput :record="record" @select="codeSelectHandler" /></td>
                        <td class="et-taskCell"><et-taskinput :record="record" @select="taskSelectHandler" /></td>
                        <td class="et-hourCell" v-for="(item,index) in record.hours" >
                            <et-hoursinput v-model="record.hours[index]"></et-hoursinput>
                        </td>
                    </tr>
                </tbody>
                <tfoot>
                    <tr>
                        <th colspan="2" class="et-addcell"><button class="btn btn-secondary" @click="newRecordEvent"><i class="icon plus"></i>Add record</button></th>
                        <th v-for="hours in totalHours" class="et-totalcell"><span :class="{'text-success': hours==8, 'text-warning': (hours<8 && hours>0), 'text-danger': hours>8}">{{hours}}</span></th>
                    </tr>
                </tfoot>
            </table>
        </div>
    `,
    computed: {
        Monday: function () { let date = new Date(); date.setTime(this.week.startDate.getTime()); return date; },
        Tuesday: function () { let date = new Date(); date.setTime(this.week.startDate.getTime() + 1000 * 60 * 60 * 24 * 1); return date; },
        Wednesday: function () { let date = new Date(); date.setTime(this.week.startDate.getTime() + 1000 * 60 * 60 * 24 * 2); return date;  },
        Thusday: function () { let date = new Date(); date.setTime(this.week.startDate.getTime() + 1000 * 60 * 60 * 24 * 3); return date; },
        Friday: function () { let date = new Date(); date.setTime(this.week.startDate.getTime() + 1000 * 60 * 60 * 24 * 4); return date; },
        totalHours: function () {
            let results = [];
            for (let day = 0; day < 5; day++) {
                results[day] = 0;
                for (let record of this.week.records.values()) {
                    let hours = Number(record.hours[day]);
                    if (isNaN(hours)) continue;
                    results[day] += hours;
                }
            }
            return results;
        }
    },
    methods: {
        newRecordEvent: function () {
            this.week.records.push({
                code: "",
                task: -1,
                taskTitle:"",
                hours:["","","","",""]
            });
        },
        codeSelectHandler: function (event) {
            //console.log("weekeditor codeSelectHandler");
            this.$emit("codeSelect", event);
        },
        taskSelectHandler:function(event){
            //console.log("weekeditor taskSelectHandler");
            this.$emit("taskSelect", event);
        }
    }
});
Vue.component("et-editor", {
    props: ["etimes", "timespan"],
    data: function () {
        return {
            weeks: [],
            codeModalId: "modal-3f28e3cb-83d3-414c-92e5-7d2d800f7547",
            codeModalStatus: "",
            codeModalCodes:[],
            codeModalRefRecord:null,
            taskModalId:'modal-6341f165-e9de-403a-8c7d-136704fab010',
            taskModalStatus: "",
            taskModalTasks:[],
            taskModalRefRecord:null,
            submitModalId:"modal-a3281651-3301-493c-9d5e-b20bef65e30b",
            submitEtimes:[],
            submitErrorMessage:"",
            submitModalStatus:""
        };
    },
    template: `
        <div>
            <et-weekeditor v-for="week in weeks" :week="week" :editor="this" @codeSelect="codeSelectHandler" @taskSelect="taskSelectHandler" />
            <button class="btn btn-primary" @click="submiteHandler">Submit</button>
            <div class="modal fade et-codeModal" tabindex="-1" role="dialog" :id="codeModalId">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h4 class="modal-title">Select code:</h4>
                            <button type="button" class="close" data-dismiss="modal"><span>&times;</span></button>
                        </div>
                        <div class="modal-body">
                            <div class="alert alert-danger" role="alert" v-if="codeModalStatus=='error'">
                                Fail to get codes from the server...
                            </div>
                            <div class="alert alert-info" role="alert" v-if="codeModalStatus=='running'">
                                <div class="spinner-grow spinner-grow-sm text-info" role="status">
                                    <span class="sr-only">Loading...</span>
                                </div>
                                Searching codes from the server...
                            </div>
                            <div v-if="codeModalStatus=='success'">
                                <p>Operation codes:</p>
                                <div class="card mb-2">
                                    <ul class="list-group list-group-flush">
                                        <li class="list-group-item list-group-item-action" v-for="code in codeModalOperationCodes" @click="codeModalSelectHandler(code)">
                                            <div class="d-flex justify-content-between">
                                                <strong style="width:10em">{{code.code}}</strong>
                                                <small class="flex-fill">{{code.title}}</small>
                                            </div>
                                        </li>
                                    </ul>
                                </div>
                                <p>Project codes:</p>
                                <div class="card mb-2">
                                    <ul class="list-group list-group-flush">
                                        <li class="list-group-item list-group-item-action" v-for="code in codeModalProjectCodes" @click="codeModalSelectHandler(code)">
                                            <div class="d-flex justify-content-between">
                                                <strong style="width:10em">{{code.code}}</strong>
                                                <small class="flex-fill">{{code.title}}</small>
                                            </div>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal fade et-taskModal" tabindex="-1" role="dialog" :id="taskModalId">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h4 class="modal-title">Select task:</h4>
                            <button type="button" class="close" data-dismiss="modal"><span>&times;</span></button>
                        </div>
                        <div class="modal-body">
                            <div class="alert alert-danger" role="alert" v-if="taskModalStatus=='error'">
                                Fail to get tasks from the server...
                            </div>
                            <div class="alert alert-info" role="alert" v-if="taskModalStatus=='running'">
                                <div class="spinner-grow spinner-grow-sm text-info" role="status">
                                    <span class="sr-only">Loading...</span>
                                </div>
                                Searching tasks from the server...
                            </div>
                            <div v-if="taskModalStatus=='success'">
                                <div class="card mb-2">
                                    <ul class="list-group list-group-flush">
                                        <li class="list-group-item list-group-item-action" v-for="task in taskModalTasks" @click="taskModalSelectHandler(task)">
                                            <div class="d-flex justify-content-between">
                                                <strong style="width:10em">{{task.number}}</strong>
                                                <small class="flex-fill">{{task.title}}</small>
                                            </div>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal fade et-taskModal" tabindex="-1" role="dialog" :id="submitModalId">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h4 class="modal-title">Submit</h4>
                            <button type="button" class="close" data-dismiss="modal"><span>&times;</span></button>
                        </div>
                        <div class="modal-body">
                            <div class="alert alert-danger" role="alert" v-if="submitModalStatus=='error'">
                                Submit Error! <br /> {{submitErrorMessage}}
                            </div>
                            <div class="alert alert-info" role="alert" v-if="submitModalStatus=='running'">
                                <div class="spinner-grow spinner-grow-sm text-info" role="status">
                                    <span class="sr-only">Submit in progress...</span>
                                </div>
                                Searching tasks from the server...
                            </div>
                            <div class="alert alert-success" v-if="submitModalStatus=='success'">
                                <p>Submit is success! {{submitCount}} records are submitted.
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-primary" @click="submitModalConfirmHandler">OK</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>`,
    watch: {
        etimes: function (val) {
            if (this.etimes!==null && this.timespan!==null)
                this.weeks = this.getWeeks();
        },
        timespan: function (val) {
            if (this.etimes!==null && this.timespan!==null)
                this.weeks = this.getWeeks();
        }
    },
    computed:{
        codeModalOperationCodes:function(){
            let codes=[];
            for(let code of this.codeModalCodes.values()){
                if (!(code.code.startsWith("PJ-"))) codes.push(code);
            }
            codes.sort(function (a, b) { return a.code.localeCompare(b.code); });
            return codes;    
        },
        codeModalProjectCodes:function(){
            let codes=[];
            for(let code of this.codeModalCodes.values()){
                if (code.code.startsWith("PJ-")) codes.push(code);
            }
            codes.sort(function (a, b) { return a.code.localeCompare(b.code); });
            return codes;
        },
        submitCount:function(){
            return this.submitEtimes.length;
        }
    },
    methods: {
        getWeeks: function () {
            try {
                let startDate = new Date(this.timespan.startDate);
                let endDate = new Date(this.timespan.endDate);

                let wkStartDate = Etime.getFirstDayOfWeek(startDate);

                let wkEndDate = Etime.getLastDayOfWeek(startDate);
                let result = [];
                while (true) {
                    // find corresponding records
                    let etimes = [];
                    {
                        this.etimes.forEach(function (etime, index) {
                            let date = new Date(etime.occurDate);
                            if (date >= wkStartDate && date <= wkEndDate) etimes.push(etime);
                        });
                    }
                    //
                    let codeTaskNameList = [];
                    {
                        //console.log("Generating unique row list for projects and tasks...");
                        for (let etime of etimes.values()) {
                            if (codeTaskNameList.findIndex(
                                function (value, index, arr) { return (value.code == this.code && value.task == this.task); }, etime) < 0) {
                                codeTaskNameList.push({ code: etime.code, task: etime.task, taskTitle: etime.taskTitle});
                                //console.log("Code: " + etime.code + "; Task: " + etime.task);
                            }
                        }
                        //console.log("Sorting the records by project code and task number...");
                        codeTaskNameList.sort(function (a, b) {
                            let astr = `${a.Code}:${a.Task}`;
                            let bstr = `${b.Code}:${b.Task}`;
                            if (!astr.startsWith("PJ-") && bstr.startsWith("PJ-")) return 1;
                            if (astr.startsWith("PJ-") && !bstr.startsWith("PJ-")) return -1;
                            return astr.localeCompare(bstr);
                        });
                        if (codeTaskNameList.length == 0) {
                            codeTaskNameList.push({
                                code: "",
                                task: -1,
                                taskTitle:""
                            });
                        }
                    }
                    // generating table data
                    //console.log('Generating table data...');
                    for (let codeTask of codeTaskNameList.values()) {
                        codeTask.hours = [];
                        for (let weekDay = 0; weekDay < 5; weekDay++) {
                            codeTask.hours[weekDay] = 0;
                            let date = new Date(); date.setTime(wkStartDate.getTime() + 1000 * 60 * 60 * 24 * weekDay);
                            for (let etime of etimes.values()) {
                                let date2 = new Date(); date2.setTime(Date.parse(etime.occurDate));
                                if (Etime.getDateString(date) == Etime.getDateString( date2) && codeTask.code==etime.code && codeTask.task==etime.task)
                                    codeTask.hours[weekDay] += etime.hours;
                            }
                            if (codeTask.hours[weekDay] == 0) codeTask.hours[weekDay] = "";
                            else codeTask.hours[weekDay] = codeTask.hours[weekDay].toString();
                        }
                    }
                    let day1 = new Date(); day1.setTime(wkStartDate.getTime());
                    let day7 = new Date(); day7.setTime(wkStartDate.getTime() + 1000 * 60 * 60 * 24 * 6);
                    result.push({
                        startDate: day1,
                        endDate: day7,
                        weekNumber: Etime.getWeekNumber(wkStartDate),
                        records: codeTaskNameList,
                    });
                    //console.log(wkStartDate);
                    wkStartDate.setTime(wkStartDate.getTime() + 7 * 24 * 60 * 60 * 1000);
                    wkEndDate.setTime(wkEndDate.getTime() + 7 * 24 * 60 * 60 * 1000);
                    if (wkStartDate > endDate) break;
                }
                console.log("Getting reorganized etimes...")
                console.log(result);
                return result;
            }
            catch (e) {
                console.log(e);
                return [];
            }
        },
        codeSelectHandler:function(event){
            console.log("editor codeSelectHandler");
            this.codeModalRefRecord=event.record;
            let req = {
                function: "getCodes",
            };
            let rsp = $.ajax({
                type: "POST",
                url: "/etime/service",
                contentType: "application/json",
                data: JSON.stringify(req),
                dataType: "json",
                async: true,
                context: this,
                beforeSend: this.codeSearch_beforeCallback,
                success: this.codeSearch_successCallback,
                error: null,
                complete: null,
            }).responseJSON;
            $(`#${this.codeModalId}`).modal('show');
        },
        codeSearch_beforeCallback:function(){
            this.codeModalStatus="running";
        },
        codeSearch_successCallback:function(rsp){
            this.codeModalStatus="success";
            this.codeModalCodes=rsp.codes;
            console.log(rsp);
        },
        codeModalSelectHandler:function(code){
            $(`#${this.codeModalId}`).modal("hide");
            this.codeModalRefRecord.code=code.code;;
            this.codeModalRefRecord.task=0;
        },
        taskSelectHandler:function(event){
            console.log("editor taskSelectHandler");
            this.taskModalRefRecord=event.record;
            let req = {
                function: "getTasks",
                code: event.record.code,
            };
            let rsp = $.ajax({
                type: "POST",
                url: "/etime/service",
                contentType: "application/json",
                data: JSON.stringify(req),
                dataType: "json",
                async: true,
                context: this,
                beforeSend: this.taskSearch_beforeCallback,
                success: this.taskSearch_successCallback,
                error: null,
                complete: null,
            }).responseJSON;
            $(`#${this.taskModalId}`).modal('show');
        },
        taskSearch_beforeCallback:function(){
            this.taskModalStatus="running";
        },
        taskSearch_successCallback:function(rsp){
            this.taskModalStatus="success";
            let tasks=rsp.tasks;
            let findtask0=false;
            for (let task of tasks.values())
            {
                if (task.number==0){
                    findtask0=true;
                    break;
                }
            }
            if(!findtask0){
                tasks.push({
                    number:0,
                    title:"非特定任务"
                });
            }
            tasks.sort(function(a,b){return a.number-b.number;})
            this.taskModalTasks=rsp.tasks;
            console.log(rsp);
        },
        taskModalSelectHandler:function(task){
            $(`#${this.taskModalId}`).modal("hide");
            this.taskModalRefRecord.task=task.number;
            this.taskModalRefRecord.taskTitle=task.title;
        },
        submiteHandler:function(){
            console.info("submiteHandler")
            //console.log('submiteHandler');
            let etimes=[];
            for(week of this.weeks.values()){
                //console.log(week);
                 for(record of week.records.values()) {
                    //console.log(record);
                    for(dayIndex=0;dayIndex<5;dayIndex++) {
                        let day=new Date();day.setTime(week.startDate.getTime()+1000*60*60*24*dayIndex);
                        let hours=Number(record.hours[dayIndex]);
                        if (isNaN(hours)) continue;
                        if (hours<=0) continue;
                        etimes.push({
                            code: record.code,
                            task:record.task,
                            hours:hours,
                            occurDate:Etime.getDateString(day),
                            user:0,
                        })
                    }
                }
            }
            console.log(etimes);
            let req = {
                function: "setMyEditableEtimes",
                etimes: etimes
            };
            let rsp = $.ajax({
                type: "POST",
                url: "/etime/service",
                contentType: "application/json",
                data: JSON.stringify(req),
                dataType: "json",
                async: true,
                context: this,
                beforeSend: this.submit_beforeCallback,
                success: this.submit_successCallback,
                error: this.submit_errorCallback,
                complete: null,
            }).responseJSON;
            $(`#${this.submitModalId}`).modal('show');
        },
        submit_beforeCallback:function(){
            console.log("submit_beforeCallback");
            this.submitModalStatus="running";
        },
        submit_successCallback:function(rsp){
            console.log("submit_successCallback");
            if(!rsp.isSuccess){
                this.submitErrorMessage=rsp.exceptionMessage;
                this.submitModalStatus="error";
                return;
            }
            this.submitErrorMessage="";
            this.submitModalStatus="success";
            this.submitEtimes=rsp.etimes;
        },
        submit_errorCallback:function(){
            console.log("submit_errorCallback");
            this.submitModalStatus="error";
            this.submitErrorMessage="Erro in AJAX post.";
        },
        submitModalConfirmHandler:function(){
            $(`#${this.submitModalId}`).modal('hide');
            window.location.reload();
        }

    }
});