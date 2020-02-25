class Estaffing{
    
};
var esTable=Vue.component("es-table",{
    props:['editor'],
    template:`
    <table>
        <thead>
            <tr>
                <th>User</th>
                <th v-for="month in editor.monthes">{{month}}</th>
            </tr>
        </thead>
    </table>
    `,
});
var esEditor=Vue.component('es-editor',{
    props:['estaffings'],
    template: `
    <div class="es-editor">
    </div>
    `,
    computed:{
        monthes:function(){
            let today=new Date();
            
        }
    },
    mounted:{

    }

});