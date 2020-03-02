var esBookCell=Vue.component("es-bookcell",{
    props:["booking"],
    template:`
    <template>
        <td v-html="displayHtml"></td>
    </template>
    `,
    computed:{
        displayHtml:function(){
            if (isNaN(this.booking)) return "";
            if (this.booking==0) return "";
            let load=Math.round(this.booking/8/22*100);
            if (load<60) return `<span class="text-danger">${load}%</span>`;
            if (load<80) return `<span class="text-warning">${load}%</span>`;
            if (load<100) return `<span class="text-success">${load}%</span>`;
            else return `<span class="text-danger">${load}%</span>`;
        }
    }
});
var esSubRow=Vue.component("es-subrow",{
    props:["booking"],
    template:``,
});
var esRow=Vue.component("es-row",{
    props:["booking"],
    data:function(){
        return{
            showProjectRows:true,
        };
    },
    template:`
    <template>
        <tr>
        </tr>
        <tr>
        </tr>
    </template>
    `,
});
var esTable=Vue.component("es-table",{
    props:['editor'],
    template:`
    <table class="table table-hover table-sm table-bordered es-table">
        <thead >
            <tr>
                <th>User</th>
                <th v-for="month in editor.monthes">{{month.name}}</th>
            </tr>
        </thead>
        <tbody>
            <template v-for="booking in editor.bookings">
                <tr class="es-row">
                    <td class="es-usercell" @click="userClickHandler(booking)">{{booking.user.displayName}}<i class="float-right" :class="{'angle right icon':!isBookingSelected(booking), 'angle down icon':isBookingSelected(booking)}"></i></td>
                    <td v-for="month in booking.bookings" :booking="month" is="es-bookcell"></td>
                </tr>
                <template v-for="projectBooking in booking.projectBookings">
                    <tr class="es-subrow" :class="{'d-none': !isBookingSelected(booking)}">
                        <td class="es-projectcell">{{projectBooking.project}}</td>
                        <td v-for="booking2 in projectBooking.bookings" :booking="booking2" is="es-bookcell"></td>
                    </tr>
                </template>
            </template>
        </tbody>
    </table>
    `,
    methods:{
        userClickHandler:function(booking){
            if(this.editor.selectedBooking===booking)this.editor.selectedBooking=null;
            else this.editor.selectedBooking=booking;
        },
        isBookingSelected:function(booking){
            return booking===this.editor.selectedBooking;
        }
    }
});
var esEditor=Vue.component('es-editor',{
    props:['estaffings'],
    data:function(){
        return{
            estaffings:null,
            estaffingAjaxStatus:"",

            projects:null,
            projectAjaxStatus:"",

            users:null,
            userAjaxStatus:"",
            validUsers:[
                1,2,9,,10,11,12,13,15,23,24,25,28,35,41,43,44,45,47,48,59,60,62,66,68,69,71
            ],

            monthes:[],

            bookings:[],
            selectedBooking:null
        };
    },
    template: `
    <div class="es-editor">
        <es-table :editor="self"></es-table>
    </div>
    `,
    computed:{
        self:function(){return this;}
    },
    methods:{
        getMonthName:function(monthDate){
            switch(monthDate.getUTCMonth()){
                case 0: return "JAN";
                case 1: return "FEB";
                case 2: return "MAR";
                case 3: return "APR";
                case 4: return "MAY";
                case 5: return "JUN";
                case 6: return "JUL";
                case 7: return "AUG";
                case 8: return "SEP";
                case 9: return "OCT";
                case 10: return "NOV";
                case 11: return "DEC";
            }
        },
        loadData:function(){
            if(this.users===null || this.projects===null) return;
            let bookings=[];
            // month
            {
                this.monthes=[];
                let currentDate=DateTime.getFirstDayOfMonth();
                let pastDate=DateTime.getFirstDayOfMonth(currentDate);
                let comingDate=DateTime.getFirstDayOfMonth(currentDate);
                let pastMonthes=2;
                let comingMonthes=6;
                if(pastDate.getUTCMonth()<pastMonthes){
                    pastDate.setUTCFullYear(pastDate.getUTCFullYear()-1);
                    pastDate.setUTCMonth(pastDate.getUTCMonth()+(12-pastMonthes));
                }
                else{
                    pastDate.setUTCMonth(pastDate.getUTCMonth()-pastMonthes);
                }
                if(comingDate.getUTCMonth()>(12-1-comingMonthes)){
                    comingDate.setUTCFullYear(comingDate.getUTCFullYear()+1);
                    comingDate.setUTCMonth(comingDate.getUTCMonth()-(12-comingMonthes));
                }
                else{
                    comingDate.setUTCMonth(comingDate.getUTCMonth()+comingMonthes);
                }
                //console.log("Start date: "+pastDate.toJSON()); 
                //console.log("End date: "+comingDate.toJSON());
                currentDate.setTime(pastDate.getTime());
                let index=0;
                while(true){
                    this.monthes.push({
                        index:index,
                        date:new Date(currentDate.toJSON()),
                        dateStr:DateTime.getDateString(currentDate),
                        name:this.getMonthName(currentDate),
                    });
                    if(currentDate.getUTCMonth()>=11){
                        currentDate.setUTCFullYear(currentDate.getUTCFullYear()+1);
                        currentDate.setUTCMonth(0);
                    }
                    else{
                        currentDate.setUTCMonth(currentDate.getUTCMonth()+1);
                    }
                    index+=1;
                    if (currentDate>comingDate) break;
                }
                console.log(this.monthes);
            }
            // user
            {
                for(let user of this.users.values()){
                    if (!(this.validUsers.includes(user.id))) continue;
                    let booking={
                        user:{
                            id:user.id,
                            name:user.name,
                            displayName:user.displayName,
                        },
                        bookings:[],
                        projectBookings:[],
                    };
                    booking.bookings=new Array(this.monthes.length);
                    booking.bookings.fill(0);
                    bookings.push(booking);
                }
                bookings.sort(function(a,b){
                    return a.user.displayName.localeCompare(b.user.displayName);
                });
            }
            // project
            {
                for(let project of this.projects.values()){
                    //task
                    for(let task of project.tasks){
                        if (task.schedule===null){}
                        else if(task.schedule===""){task.schedule=null;}
                        else{
                            //console.log(task.schedule);
                            task.schedule=eval(task.schedule);
                            //console.log(task.schedule);
                        }
                        //schedule
                        if (task.schedule===null) continue;
                        for(let schedule of task.schedule){
                            let user=schedule.user;
                            let monthDate=DateTime.getFirstDayOfMonth(new Date(schedule.weekDate));
                            let hours=schedule.hours;
    
                            let dateStr=DateTime.getDateString(monthDate);
                            let booking=bookings.find(function(item){
                                return item.user.id===user;
                            });
                            if(booking===undefined || booking===null) continue;

                            let monthIndex=this.monthes.findIndex(function(item){
                                return item.dateStr===dateStr;
                            });
                            if (monthIndex<0) continue; //outof timespan
                            booking.bookings[monthIndex]+=hours;

                            let projectBooking=booking.projectBookings.find(function(item){
                                return item.project==project.code;
                            });
                            if(projectBooking===undefined || projectBooking===null){
                                projectBooking={
                                    project:project.code,
                                    bookings:new Array(this.monthes.length),
                                };
                                projectBooking.bookings.fill(0);
                                projectBooking.bookings[monthIndex]+=hours;
                                booking.projectBookings.push(projectBooking);
                            }
                            else{
                                projectBooking.bookings[monthIndex]+=hours;
                            }
                        }
                    }
                }
            }
            this.bookings=bookings;
            console.log("this.bookings:")
            console.log(this.bookings);

        },
        getEstaffing_beforeCallback:function(){
            this.estaffingAjaxStatus="running";
        },
        getEstaffing_successCallback:function (rsp) {
            console.info(`${new Date().toJSON()}: Success to get estaffing data from the server!`);
            console.log(rsp);
            if (rsp.isSuccess){
                this.estaffingAjaxStatus="success";
                this.estaffings=rsp.users;
                this.loadData();
            }
            else{
                this.estaffingAjaxStatus="error";
                this.estaffings=null;
                console.warn(rsp.exceptionMessage);
            }
        },
        getEstaffing_errorCallback:function () {
            this.estaffingAjaxStatus="error";
            this.estaffings=null;
            console.error(`${new Date().toJSON()}: Fail to fetch estaffing data from the server!`);
        },
        getProject_beforeCallback:function(){
            this.projectAjaxStatus="running";
        },
        getProject_successCallback:function (rsp) {
            console.info(`${new Date().toJSON()}: Success to get project data from the server!`);
            console.log(rsp);
            if (rsp.isSuccess){
                this.projectAjaxStatus="success";
                this.projects=rsp.projects;
                this.loadData();
            }
            else{
                this.projectAjaxStatus="error";
                this.projects=null;
                console.warn(rsp.exceptionMessage);
            }
        },
        getProject_errorCallback:function () {
            this.projectAjaxStatus="error";
            this.projects=null;
            console.error(`${new Date().toJSON()}: Fail to fetch project data from the server!`);
        },
        getUsers_beforeCallback:function(){
            this.userAjaxStatus="running";
        },
        getUsers_successCallback:function(rsp){
            console.info(`${new Date().toJSON()}: Success to get user data from the server!`);
            console.log(rsp);
            if (rsp.isSuccess){
                this.userAjaxStatus="success";
                this.users=rsp.users;
                this.loadData();
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
    },
    mounted:function(){
        $.ajax({
            type: "POST",
            url: "/estaffing/service",
            contentType: "application/json",
            data: JSON.stringify({
                function: "getEstaffings",
            }),
            dataType: "json",
            async: true,
            context: this,
            beforeSend: this.getEstaffing_beforeCallback,
            success: this.getEstaffing_successCallback,
            error: this.getEstaffing_errorCallback,
            complete: null,
        });
        $.ajax({
            type: "POST",
            url: "/project/service",
            contentType: "application/json",
            data: JSON.stringify({
                function: "getProjectSchedules",
            }),
            dataType: "json",
            async: true,
            context: this,
            beforeSend: this.getProject_beforeCallback,
            success: this.getProject_successCallback,
            error: this.getProject_errorCallback,
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
    }

});