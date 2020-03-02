class DateTime{
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
    static getFirstDayOfMonth(){
        let date;
        if (arguments.length == 1) { date = arguments[0]; } else { date = new Date(); }
        date=this.getDateComponent(date);
        let firstDate=new Date;
        firstDate.setTime(date.getTime());
        firstDate.setUTCDate(1);
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