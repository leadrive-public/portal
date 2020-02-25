class Project {
    static getDateComponent(date) {
        let newDate = new Date();
        newDate.setTime(date.getTime());
        newDate.setUTCHours(0); newDate.setUTCMinutes(0); newDate.setUTCSeconds(0); newDate.setUTCMilliseconds(0);
        return newDate;
    }
    static getFirstDayOfWeek() {
        let date;
        if (arguments.length == 1) { date = arguments[0]; } else { date = new Date(); }
        date=this.getDateComponent(date)
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
        date=this.getDateComponent(date);
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
    static isPastWeek(date){
        let today=Project.getDateComponent(new Date());
        let weekStartDate=this.getFirstDayOfWeek(date);
        let weekEndDate=this.getLastDayOfWeek(date);
        //历史周
        if(today>weekEndDate){ return true; }
        //当前周
        else if(today>weekStartDate) {
            if (today.getUTCDay()===0)
                return true;
            else if (today.getUTCDay()===6)
                return true;
            else
                return false;
        }
        //未来周
        else{ return false; }
    }
    static isCurrentWeek(date){
        let today=Project.getDateComponent(new Date());
        let weekStartDate=this.getFirstDayOfWeek(date);
        let weekEndDate=this.getLastDayOfWeek(date);
        //历史周
        if(today>weekEndDate){ return false; }
        //当前周
        else if(today>weekStartDate) {
            if (today.getUTCDay()===0)
                return false;
            else if (today.getUTCDay()===6)
                return false;
            else
                return true;
        }
        //未来周
        else{ return false; }
    }
    static isComingWeek(date){
        let today=Project.getDateComponent(new Date());
        let weekStartDate=this.getFirstDayOfWeek(date);
        let weekEndDate=this.getLastDayOfWeek(date);
        //历史周
        if(today>weekEndDate){ return false; }
        //当前周
        else if(today>weekStartDate) {return false;}
        //未来周
        else{ return true; }
    }
}
var gcUserSelect=Vue.component("gc-userselector",{
    props:["users", "value","readonly"],
    data:function(){
        return{
            matchedUsers:null,
            inputText:"",
        };
    },
    template:`
    <div>
        <div class="input-group">
            <input type="text" class="form-control" v-model="inputText" @input="inputHandler" :readonly="readonly?'readonly':false" />
        </div>
        <div class="dropdown">
            <button class="btn btn-outline-secondary dropdown-toggle d-none" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-popperConfig=""></button>
            <div class="dropdown-menu">
                <div class="dropdown-item" v-for="user in matchedUsers" @click="optionClickHandler(user)">{{getOptionText(user)}}</div>
            </div>
        </div>
    </div>
    `,
    watch:{
        users:function(val){
            let inputText=this.getInputText(); 
            if (inputText!==this.inputText) this.inputText=inputText;
        },
        value:function(val){
            let inputText=this.getInputText(); 
            if (inputText!==this.inputText) this.inputText=inputText;
        },
        inputText:function(val){
            for(let user of this.users.values()){
                if (user.displayName===val && this.value!==user.id){
                    this.$emit('input', user.id);
                }
            }
        }
    },
    mounted:function(){
        let inputText=this.getInputText(); 
        if (inputText!==this.inputText) this.inputText=inputText;
    },
    methods: {
        inputHandler: function (event) {
            console.log("inputHandler");
            let $dropdown=$(this.$el);
            let $input= $dropdown.find("input");
            let $dropdownMenu=$dropdown.find(".dropdown-menu");
            try{
                if ($input.val() !=""){
                    let matchedUsers=[];
                    for (let user of this.users.values()){
                        if (user.name.includes($input.val()) || user.displayName.includes($input.val())){
                            matchedUsers.push(user);
                        }
                    }
                    this.matchedUsers=matchedUsers;
                    $dropdownMenu.dropdown('show');
                }
                else{
                    $dropdownMenu.dropdown('hide');
                }
            }
            catch(e){
                console.log(e);
            }
            $input.focus() ;
        },
        getOptionText:function(user){
            return user.displayName+"<"+user.name+">";
        },
        getInputText:function(){
            console.log("getInputText");
            if (this.users ===null || this.value===null) { return ""; }
            if (this.value<=0) { return ""; }
            for(let user of this.users.values()){
                if (user.id==this.value) { return  `${user.displayName}`; }
            }
            return `${this.value}`;
        },
        optionClickHandler:function(user){
            console.log("optionClickHandler");
            let $dropdown=$(this.$el);
            let $dropdownMenu=$dropdown.find(".dropdown-menu");
            $dropdownMenu.dropdown('hide');
            this.$emit('input', user.id);
            console.log(user.id);
            console.log("optionClickHandler2");
        }
    }
})
var gcNoCell=Vue.component("gc-nocell",{
    data: function(){
        return{
            delay: 400,
            clicks: 0,
            timer: null,
        }
    },
    props:["task","isHeader", "editor"],
    template:`
    <template>
        <th class="gc-nocell" v-if="isHeader" >No.</th>
        <td class="gc-nocell" :class="{'gc-grouptask':task.isGrouped }"  @click="clickHandler" v-else >{{displayValue}}</td>
    </template>
    `,
    computed:{
        isTaskSelected: function(){if (this.editor.selectTask===this.task){return true;} else{return false;}},
        displayValue:function(){if (!("number" in this.task)){ return "*";} if (this.task.number<0) { return "*";} return this.task.number;}
    },
    methods:{
        clickHandler:function(){
            this.clicks++;
            if(this.clicks === 1) {
                let self = this;
                this.timer = setTimeout(function() {
                    self.clicks = 0;
                }, this.delay);
                this.$emit("click",this);
            } else{
                clearTimeout(this.timer);
                this.$emit("dblclick",this);
                this.clicks = 0;
            }         
        }
    }
});
var gcTitleCell=Vue.component("gc-titlecell",{
    data: function(){
        return{
            delay: 400,
            clicks: 0,
            timer: null,
        }
    },
    props:["task","isHeader", "editor"],
    template:`
        <template>
            <th class="gc-titlecell" v-if="isHeader" >Title</th>
            <td class="gc-titlecell"  @click="clickHandler" v-else>
                <div v-if="!isActiveCell" :class="{'gc-grouptask':task.isGrouped }">{{task.title}}</div>
                <input v-else v-model="task.title"  />
            </td>
        </template>
    `,
    computed:{
        isTaskSelected: function(){if (this.editor.selectTask===this.task){return true;} else{return false;}},
        isActiveCell:function(){return(this.editor.activeCell===this);}
    },
    methods:{
        clickHandler:function(){
            if(!this.isActiveCell){
                this.editor.activeCell=this;
                this.$emit("click",this);
            }  
        }
    }
});
var gcStatusCell=Vue.component("gc-statuscell",{
    props:["task","isHeader","editor"],
    template:`
        <template>
            <th class="gc-statuscell" v-if="isHeader" >Stat.</th>
            <td class="gc-statuscell" v-else @click="clickHandler" >
                <template v-if="!isGroupedTask">
                    <div :class="[bgClass]" v-if="!isActiveCell">{{status}}</div>
                    <select v-model="task.status" v-else>
                        <option value=""></option>
                        <option value="todo">todo</option>
                        <option value="done">done</option>
                        <option value="closed">closed</option>
                        <option value="ongoing">ongoing</option>
                    </select>
                </template>
            </td>
        </template>
    `,
    computed:{
        isTaskSelected: function(){if (this.editor.selectTask===this.task){return true;} else{return false;}},
        status: function(){
            if (this.task === null) return "";
            if ("status" in this.task) return this.task.status;
            return "";
        },
        isGroupedTask:function(){
            try{ return this.task.isGrouped; }
            catch(e) {return true;}
        },
        bgClass: function(){
            if (this.status==="done") return "gc-bg-green";
            if (this.status==="closed") return "gc-bg-green";
            if (this.status==="ongoing") return "gc-bg-yellow";
            return "";
        },
        isActiveCell:function(){return(this.editor.activeCell===this);}
    },
    methods:{
        clickHandler:function(){
            if(!this.isActiveCell){
                this.editor.activeCell=this;
                this.$emit("click",this);
            }
        }
    }
});
var gcWeekCell=Vue.component("gc-weekcell",{
    data: function(){
        return{
            delay: 400,
            clicks: 0,
            timer: null,
            etimeHoursZ:0,
            taskZ:null,
            weekZ:null,
        }
    },
    props:["task","isHeader", "week", "editor"],
    template:`
        <template>
            <th class="gc-weekcell" :title="timeRangeTitle" v-if="isHeader" :class="[hiddenCellClass]">W{{week.weekNumber}}</th>
            <td class="gc-weekcell" v-else @click="clickHandler" :class="[bgClass, hiddenCellClass]" >
                <template v-if="!(task.isGrouped)">{{displayValue}}</template>
            </td>
        </template>
    `,
    computed:{
        isHiddenCell:function(){
            if (!this.editor.showAllPastWeeks && this.week.isLongPastWeek) return true;
            if (!this.editor.showAllComingWeeks && this.week.isLongComingWeek) return true;
            return false;
        },
        hiddenCellClass:function(){
            if (this.isHiddenCell) return "gc-hiddenCell";
            else return "";
        },
        isTaskSelected: function(){if (this.editor.selectTask===this.task){return true;} else{return false;}},
        timeRangeTitle: function(){return "from " + Project.getDateString(this.week.startDate) + ' to ' + Project.getDateString(this.week.endDate);},
        isActiveCell:function(){return(this.editor.activeCell===this);},
        displayValue:function(){
            let weekStartDate=this.week.startDate;
            //历史周
            if(Project.isPastWeek(weekStartDate)){
                if (this.etimeHours>0){ return (Math.round(this.etimeHours/40*10)/10); }
                else{ return "" }
            }
            //当前周
            else if(Project.isCurrentWeek(weekStartDate)){
                if (this.etimeHours>0){ return (Math.round(this.etimeHours/40*10)/10); }
                else{ return "" }
            }
            //未来周
            else {
                if(this.plannedHours>0){
                    return (Math.round(this.plannedHours/40*10)/10).toFixed(1);
                }
                else{
                    return "";
                }
            }
        },
        etimeHours:function(){return this.getEtimeHours(); },
        plannedHours:function(){return this.getPlannedHours();},
        bgClass:function(){
            let weekStartDate=this.week.startDate;
            //历史周
            if(Project.isPastWeek(weekStartDate)){
                if (this.etimeHours>0){ return "gc-bg-green"; }
                else{ return "gc-bg-lightgray" }
            }
            //当前周
            else if(Project.isCurrentWeek(weekStartDate)){
                if (this.etimeHours>0){ return "gc-bg-yellow"; }
                else{ return "" };
            }
            //未来周
            else {
                if (this.plannedHours>0){ return "gc-bg-lightGreen"; }
                else{ return "" };
            }
        }
    },
    methods:{
        clickHandler:function(){
            this.clicks++;
            if(this.clicks === 1) {
                let self = this;
                this.timer = setTimeout(function() {
                    self.clicks = 0;
                }, this.delay);
                if(!this.isActiveCell){
                    this.editor.activeCell=this;
                    this.editor.selectWeek=this.week;
                }
                this.$emit("click",this);
            } else{
                clearTimeout(this.timer);
                if (!this.task.isGrouped) this.editor.weekInputShowHandler();
                this.$emit("dblclick",this);
                this.clicks = 0;
            }         
        },
        getEtimeHours:function(){
            let startDate=this.week.startDate;
            let endDate=this.week.endDate;
            let task=this.task.number;
            let hours=0;
            this.editor.etimes.forEach(function(item,index){
                let occurDate=new Date(item.occurDate);
                if (item.task==task && occurDate>startDate && occurDate<endDate) {
                    hours+=item.hours;
                }
            });
            return hours;
        },
        getPlannedHours:function(){
            let startDate=this.week.startDate;
            let weekDateStr=Project.getDateString(Project.getFirstDayOfWeek(startDate));
            let hours=0;
            if(!('schedule' in this.task)) return 0;
            if (this.task.schedule===null) return 0;
            for(let item of this.task.schedule.values()){
                if ( item.weekDate===weekDateStr) hours+=item.hours;
            }
            return hours;
        }
    }
});
var gcEtimeCell=Vue.component("gc-etimecell",{
    props:["task","isHeader","editor"],
    template:`
    <template>
        <th class="gc-etimecell" v-if="isHeader" >Spend</th>
        <td class="gc-etimecell" v-else >
            <template v-if="!(task.isGrouped)">{{displayValue}}</template>
        </td>
    </template>
    `,
    computed:{
        displayValue:function(){
            let hours=0;
            let task=this.task.number;
            this.editor.etimes.forEach(function(item,index){
                let occurDate=new Date(item.occurDate);
                if(item.task==task){
                    hours+=item.hours;
                }
            });
            return (hours/40).toFixed(1);
        }
    }
});
var gcBudgetCell=Vue.component("gc-budgetcell",{
    props:["task","isHeader","editor"],
    template:`
    <template>
        <th class="gc-budgetcell" v-if="isHeader">Budget</th>
        <td class="gc-budgetcell" v-else @click="clickHandler" >
            <template v-if="!task.isGrouped">
                <input type="number" v-model.number="task.budget" :readonly="isActiveCell?false:'readonly'"/>
            </template>
        </td>
    </template>`,
    computed:{
        isActiveCell:function(){return(this.editor.activeCell===this);}
    },
    methods:{
        clickHandler:function(){
            if(!this.isActiveCell){
                this.editor.activeCell=this;
                this.$emit("click",this);
            }  
        }
    }
});
var gcRow=Vue.component("gc-row",{
    props:["project", "task","isHeader","editor"],
    template:`
    <tr class="gc-row" :class="{'gc-selected':isTaskSelected}" >
        <td :task="task" :isHeader="isHeader" :editor="editor" @click="clickHandler" is="gc-nocell" ></td>
        <td :task="task" :isHeader="isHeader" :editor="editor" @click="clickHandler" is="gc-titlecell"></td>
        <td :task="task" :isHeader="isHeader" :editor="editor" @click="clickHandler" is="gc-statuscell"></td>
        <td :task="task" :isHeader="isHeader" :editor="editor" @click="clickHandler" is="gc-budgetcell"></td>
        <td :task="task" :isHeader="isHeader" :editor="editor" @click="clickHandler" is="gc-etimecell"></td>
        <td :task="task" :isHeader="isHeader" :editor="editor" @click="clickHandler" is="gc-weekcell" v-for="week in editor.weeks" v-bind:week="week"></td>
    </tr>
    `,
    computed:{
        isTaskSelected: function(){if (this.editor.selectTask===this.task){return true;} else{return false;}},
    },
    methods:{
        clickHandler:function(){
            //console.log("clickHandler");
            this.editor.selectTask=this.task;
            this.$emit("select", this);
        },
    }
})
var gcTable=Vue.component("gc-table",{
    props:["project", "isMask","scrollLeft", "editor"],
    template:`
        <table class="ganttchart-table" v-bind:class="{'ganttchart-table-fixedColMask':isMask}" v-bind:style="{left: scrollLeft+'px'}">
            <thead>
                <tr is="gc-row" :project="project" :task="null" :isHeader="true" :editor="editor"></tr>
            </thead>
            <tbody>
                <tr is="gc-row" :project="project" :task="task" :isHeader="false" :editor="editor" v-for="task in project.tasks"></tr>
            </tbody>
        </table>
    `,
    methods:{

    }
})
var gcTableView=Vue.component("gc-tableview",{
    props:["project","editor"],
    data:function () {
        return {
            scrollLeft: 0
        }
    },
    template:`
        <div class="gc-ganttchart" v-on:scroll="scrollHandler">
            <gc-table :project="project" :isMask="false" :editor="editor" scrollLeft="0" ></gc-table>
            <gc-table :project="project" :isMask="true" :editor="editor" :scrollLeft="scrollLeft" ></gc-table>
        </div>`,
    methods:{
        scrollHandler: function(event){
            this.scrollLeft=event.target.scrollLeft;
        },
    },
    computed:{

    }
});
var gcSchdModalPlannedField=Vue.component("gc-schdmodal-plannedfield",{
    props:['value','readonly'],
    data: function(){
        return {
            bgClass:"",
        };
    },
    template:`
        <div class="input-group">
            <input class="form-control" type="text" :readonly="readonly?'readonly':false" :class="[bgClass]" :value="displayValue" @change="changeHandler" placeholder=""/>
        </div>
    `,
    computed:{
        displayValue: function () {
            if (this.value===null) return 0;
            return this.value.toFixed(1);
        },
    },
    methods:{
        changeHandler: function (event) {
            let inputValueStr=event.target.value;
            let inputValue = Number(inputValueStr);
            if (isNaN(inputValue)) {
                this.bgClass = "bg-danger";
            }
            else {
                if (inputValue < 0 || inputValue > 1) {
                    this.bgClass = "bg-danger";
                }
                else {
                    this.bgClass = "";
                }
                inputValue = Math.round(inputValue / 0.1) * 0.1;
            }
            this.$emit('input', inputValue);
        }
    }
});
var gcSchdModalActualField=Vue.component("gc-schdmodal-actualfield",{
    props:['value'],
    data: function(){
        return {
            bgClass:"",
        };
    },
    template:`
        <div class="input-group">
            <input class="form-control" type="text" readonly="readonly" :class="[bgClass]" :value="value" @changed="changeHandler" placeholder=""/>
        </div>
    `,
    methods:{
        changeHandler:function(event){
            let inputValueStr=event.target.value;
            let inputValue = Number(inputValueStr);
            if (isNaN(inputValue)) {
                this.bgClass = "bg-danger";
            }
            else {
                if (inputValue < 0 || inputValue > 5) {
                    this.bgClass = "bg-danger";
                }
                else {
                    this.bgClass = "";
                }
                inputValue = Math.round(inputValue / 0.5) * 0.5;
            }
            this.$emit('input', inputValue);
        }
    }
});
var gcEditor=Vue.component("ganttchart-editor", {
    props: ["project", "etimes", "estaffings", "users"],
    data:function() {
        return {
            selectTask:null,
            selectWeek:null,
            activeCell:null,
            title2input:"fa",
            status2input:"",
            showAllPastWeeks:false,
            showAllComingWeeks:false,
            schdModalId:"modal-16bf6d48-14d1-4c06-9b86-5ad90860b9ae",
            schdModalData:[],
            selectedUser: 1,
        }
    },
    template: `
        <div>
            <h1>{{project.code}}</h1>
            <div class="gc-toolbar">
                <button class="btn btn-primary mr-1" @click="saveHander"><i class="save icon"></i>Save</button>
                <div class="btn-group mr-1">
                    <button class="btn btn-secondary" @click="newTaskHander"><i class="plus icon"></i></button>
                    <button class="btn btn-secondary" @click="moveUpTaskHander"><i class="arrow up icon"></i></button>
                    <button class="btn btn-secondary" @click="moveDownTaskHander"><i class="arrow down icon"></i></button>
                    <button class="btn btn-secondary" @click="outdentTaskHander" :class="{'active': isGroupedTask}"><i class="outdent icon"></i></button>
                </div>
                <div class="btn-group mr-1">
                    <button class="btn btn-secondary" title="Show closed tasks" disabled><span style="width:1.18rem;display:inline-block">C</span></button>
                    <button class="btn btn-secondary" title="Show all past weeks" @click="showAllPastClickHandler" :class="{'active': showAllPastWeeks}"><i class="angle double left icon"></i></button>
                    <button class="btn btn-secondary" title="Show all past weeks" @click="showAllComingClickHandler" :class="{'active': showAllComingWeeks}"><i class="angle double right icon"></i></button>
                </div>
                <div class="btn-group mr-1">
                    <button class="btn btn-secondary" title="Show planned labors" disabled><i class="yen sign icon"></i>P</button>
                    <button class="btn btn-secondary" title="Show spend labors" disabled><i class="yen sign icon"></i>S</button>
                    <button class="btn btn-secondary" title="Show estimated labors" disabled><i class="yen sign icon"></i>E</button>
                    <button class="btn btn-secondary" title="Show progress" disabled><i class="percent icon"></i></button>
                    <button class="btn btn-secondary" title="Show task owner" disabled><i class="user icon"></ic></button>
                </div>
            </div>
            <gc-tableview  class="gc-ganttchart" :project="project" :editor="self"></gc-tableview>
            <div class="modal fade" tabindex="-1" role="dialog" :id="schdModalId">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h4 class="modal-title">Select code:</h4>
                            <button type="button" class="close" data-dismiss="modal"><span>&times;</span></button>
                        </div>
                        <div class="modal-body">
                            <table class="ui compact celled table">
                                <thead>
                                    <tr>
                                        <th>User</th>
                                        <th>Planned (week)</th>
                                        <th>Actual (week)</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="item in schdModalData">
                                        <td><gc-userselector :users="users" v-model="item.user" :readonly="schdModalReadonly"></gc-userSelector></td>
                                        <td><gc-schdmodal-plannedfield v-model="item.plannedWeeks" :readonly="schdModalReadonly" /></td>
                                        <td><gc-schdmodal-actualfield v-model="item.actualWeeks" /></td>
                                    </tr>
                                    <tr colspan="3" v-if="(schdModalData.length==0)">
                                        <td>No records.</td>
                                    </tr>
                                </tbody>
                                <tfoot>
                                    <tr>
                                        <th><button class="btn btn-secondary" @click="schdModalAddSchdHandler" :disabled="schdModalReadonly?'disabled':false"><i class="icon plus"></i></button></th>
                                        <th>0</th>
                                        <th>0</th>
                                    </tr>
                                </tfoot>
                            </table>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" @click="schdModalOkClickHandler">OK</button>
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>`,
    computed:{
        self:function(){return this},
        schdModalReadonly:function(){
            if (this.selectWeek===null) return false;
            if(!("startDate" in this.selectWeek)) return false;
            if(Project.isComingWeek(this.selectWeek.startDate)){
                return false;
            }
            else{
                return true;
            }
        },
        isGroupedTask:function(){try{return this.selectTask.isGrouped}catch(e){return false;}},
        weeks:function(){
            if (this.projects===null || this.users===null ) return [];
            let startDate=new Date();
            let endDate=new Date();
            try{
                startDate.setTime(new Date(this.project.duration.start));
                endDate.setTime(new Date(this.project.duration.end));
            }
            catch(e){
                startDate=new Date();
                endDate.setTime(startDate.getTime()+1000*60*60*24*7*4);
            }
            this.etimes.forEach(function(item,index){
                if ((new Date(item.occurDate))<startDate) {startDate=new Date(item.occurDate);}
                if ((new Date(item.occurDate))>endDate) {endDate=new Date(item.occurDate);}
            });
            let today=new Date();
            let recentPastWeekDate=new Date();
            recentPastWeekDate.setTime(today.getTime()-1000*60*60*24*7*4);
            let recentComingWeekDate=new Date();
            recentComingWeekDate.setTime(today.getTime()+1000*60*60*24*7*8);
            if(endDate<recentComingWeekDate) {endDate.setTime(recentComingWeekDate.getTime());}

            let wkStartDate=Project.getFirstDayOfWeek(startDate);
            let wkEndDate=Project.getLastDayOfWeek(startDate);
            let result=[];
            while(true)
            {
                let day1=new Date();
                day1.setTime(wkStartDate.getTime());
                let day2=new Date();
                day2.setTime(wkEndDate.getTime());
                result.push({
                    startDate: day1, 
                    endDate:  day2, 
                    weekNumber: Project.getWeekNumber(day1),
                    isLongPastWeek: day2<recentPastWeekDate,
                    isLongComingWeek: day1>recentComingWeekDate,
                });
                wkStartDate.setTime(wkStartDate.getTime() + 7 * 24 * 60 * 60 * 1000);
                wkEndDate.setTime(wkEndDate.getTime() + 7 * 24 * 60 * 60 * 1000);
                if (wkStartDate > endDate) break;
            }
            //console.log("Calculated weeks:")
            //console.log(result);
            return result;
        }
    },
    methods:{
        saveHander: function(){
            console.info((new Date()).toTimeString()+": Submit to the server!");
            console.log(this.project);
            let req ={
                function: "setProjectSchedule",
                project: this.project,
            };
            let rsp = $.ajax({
                type: "POST",
                url: "service",
                contentType: "application/json",
                data: JSON.stringify(req),
                dataType: "json",
                async: true,
                context: this,
                beforeSend: null,
                success: this.setProjectSchedule_successCallback,
                error: this.setProjectSchedule_errorCallback,
                complete: null,
            }).responseJSON;
        },
        setProjectSchedule_successCallback:function(){
            console.info((new Date()).toTimeString()+": Success to update project schedule to the server!");
            window.location.reload();
        },
        setProjectSchedule_errorCallback:function(){
            console.error(`Fail to update project schedule to the server!`);
        },
        newTaskHander: function(){
            //console.log("newTaskHander");
            let i=0;
            for (i=0;i<this.project.tasks.length;i++){
                if(this.project.tasks[i]===this.selectTask){
                    break;
                }
            }
            this.project.tasks.splice(i,0,{
                id:0,
                isGrouped:0,
                number:-1,
                title:"new task",
                status:"todo",
                schedule:null
            });
        },
        moveUpTaskHander:function(){
            console.log("moveUpTaskHander");
            this.activeCell=null;
            for(let i=0;i<this.project.tasks.length; i++){
                if(this.project.tasks[i]===this.selectTask){
                    if (i==0) 
                        return;
                    this.project.tasks.splice(i,1);
                    this.project.tasks.splice(i-1,0,this.selectTask);
                    //console.log(this.project.tasks);
                    return;
                }
            }
        },
        moveDownTaskHander:function(){
            console.log("moveDownTaskHander");
            this.activeCell=null;
            for(let i=0;i<this.project.tasks.length; i++){
                if(this.project.tasks[i]===this.selectTask){
                    if(i==this.project.tasks.length-1) 
                        return;
                    this.project.tasks.splice(i,1);
                    this.project.tasks.splice(i+1,0,this.selectTask);
                    return;
                }
            }
        },
        outdentTaskHander:function(){
            console.log("outdentTaskHander");
            if(this.selectTask!==null){
                this.selectTask.isGrouped=!this.selectTask.isGrouped;
            }
        },
        dblclickTitleHandler:function(){
            console.log("gc-editor: dblclickTitleHandler");
            this.title2input=this.selectTask.title;
            $("#titleInputModal").modal("show");
        },
        titleInputShowHandler:function(){
            console.log("titleInputShowHandler");
        },
        titleInputSubmitHandler:function(){
            console.log("Title input submitted.");
            this.selectTask.title=this.title2input;
            $('#titleInputModal').modal('hide');
        },
        titleInputCancelHandler:function(){
            $('#titleInputModal').modal('hide');
        },
        weekInputShowHandler:function(){
            console.log("weekInputShowHandler");
            // generate the temporary data
            // {user, plannedHours, actualHours}
            this.schdModalData=[];
            let schdModalData=this.schdModalData;
            let task=this.selectTask;
            if (!('schedule' in task)) task.schedule=null
            let schedule=task.schedule;
            let week=this.selectWeek;
            try{
                if (schedule===null){

                }
                else{
                    for (let schdItem of schedule.values()){
                        if (schdItem.weekDate===Project.getDateString(week.startDate)){
                            let existingItem=null;
                            for(let item of schdModalData.values()){
                                if (schdItem.user===item.user) { existingItem=item;   break; }
                            }
                            if (existingItem!=null){ 
                                existingItem.plannedHours+=schdItem.hours;
                                existingItem.plannedDays+=schdItem.hours/8;
                                existingItem.plannedWeeks+=schdItem.hours/40;
                            }
                            else{
                                schdModalData.push({
                                    user: schdItem.user,
                                    plannedHours: schdItem.hours,
                                    plannedDays: schdItem.hours/8,
                                    plannedWeeks: schdItem.hours/40,
                                    actualHours:0,
                                    actualDays:0,
                                    actualWeeks:0,
                                });
                                
                            }
                        }
                    }
                }
            }
            catch(e){
                console.log(e);
            }
            try{
                if (this.etimes !==null)
                {
                    let projectCode="PJ-"+this.project.code;
                    for (let etime of this.etimes.values()){
                        if(!((new Date(etime.occurDate))>=week.startDate && ((new Date(etime.occurDate))<=week.endDate))) continue;
                        //{code, task, user, hours, occurDate}
                        if (etime.code==projectCode && etime.task==task.number){
                            let existingItem=null;
                            for(let item of schdModalData.values()){
                                if (etime.user==item.user) { existingItem=item;   break; }
                            }
                            if (existingItem!=null){
                                existingItem.actualHours+=etime.hours;
                                existingItem.actualDays+=etime.hours/8;
                                existingItem.actualWeeks+=etime.hours/40;
                            }
                            else{ 
                                schdModalData.push({
                                    user: etime.user,
                                    plannedHours: 0,
                                    plannedDays:0,
                                    plannedWeeks:0,
                                    actualHours: etime.hours,
                                    actualDays:etime.hours/8,
                                    actualWeeks:etime.hours/40,
                                });
                            }
                        }
                    }
                }
            }
            catch(e){
                console.log(e);
            }
            console.log(this.schdModalData);
            $(`#${this.schdModalId}`).modal('show');
        },
        schdModalAddSchdHandler:function(){
            this.schdModalData.push({
                user: 0,
                plannedWeeks: 0,
                actualWeeks: 0
            })
        },
        schdModalOkClickHandler:function(){
            if (this.schdModalReadonly){
                this.schdModalData=[];
                $(`#${this.schdModalId}`).modal('hide');
                return;
            }
            let schdModalData=this.schdModalData;
            let task=this.selectTask;
            let week=this.selectWeek;
            if (!('schedule' in task)) task.schedule=[];
            if (task.schedule===null) task.schedule=[];
            // delete existing items
            if (task.schedule!==null){
                for(let index=0;index<task.schedule.length;index++){
                    if (task.schedule[index].weekDate===Project.getDateString(week.startDate)){
                        task.schedule.splice(index,1);
                    }
                }
            }
            // insert items
            for(let item of schdModalData.values()){
                task.schedule.push({
                    weekDate:Project.getDateString(week.startDate),
                    user: item.user,
                    hours: item.plannedWeeks*40,
                });
            }
            console.log(task.schedule);
            this.schdModalData=[];
            $(`#${this.schdModalId}`).modal('hide');
        },
        getUserDisplayNameFromId: function(id){
            for(user in this.users){
                if(user.id==id) return user.displayName;
            }
            return "";
        },
        weekInputCancelHandler:function(){
            $('#weekInputModal').modal('hide');
        },
        weekInputGetActualHours:function(user){
            let task=this.selectTask.number;
            let project="PJ-"+this.project.code;
            let hours=0;
            let week=this.selectWeek;
            for(item in this.etime){
                if ( item.code==project && item.task==task && item.occurDate>=week.startDate && item.occurDate<=week.endDate){
                    hours+=item.hours;
                }
            }
            return hours;
        },
        showAllPastClickHandler:function(){
            this.showAllPastWeeks=!this.showAllPastWeeks;
        },
        showAllComingClickHandler:function(){
            this.showAllComingWeeks=!this.showAllComingWeeks;
        },
        userInputSearch:function(queryString, cb){
            let users = this.users;
            let results = queryString ? users.filter(this.createUserFilter(queryString)) : users;
            // 调用 callback 返回建议列表的数据
            cb(results);
        },
        createUserFilter:function(queryString){
            return function(user) {
                let queryString2=queryString.toLowerCase();
                return (user.name.toLowerCase().includes(queryString2) || user.displayName.toLowerCase().includes(queryString2));
            };
        },
        userInputSelectHandler:function(item){

        }
    },
    watch:{
        selectedUser:function(val){
            console.log(`selectedUser=${this.selectedUser}`);
        }
    }
});
