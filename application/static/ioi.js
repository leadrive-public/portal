Vue.component("ioi-post",{
    props:["user", "content", "edittime"],
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
            <div class="align-self-end small">{{edittime}}</div>
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