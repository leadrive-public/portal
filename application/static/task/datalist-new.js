var tableDef = {
    name: "tasks",
    url: "/task/data/tasks",
    fields: [
        {
            name: "title",
            type: "text",
            dataType: "string",
            title: "Title",
            required: true,
        },
        {
            name: "description",
            type: "textarea",
            dataType: "string",
            required: true,
        },
        {
            name: "department",
            type: "list",
            dataType: "string",
            required: true,
            dataSource: {
                url: "/task/data/accessibleDepartments",
                filters: [],
            },
            binding: {
                value: "name",
                text: "title"
            }
        },
        {
            name: "type",
            type: "list",
            dataType: "string",
            required: true,
            dataSource: {
                url: "/task/data/taskTypes",
                filters: ["department"]
            }
        },
        {
            name: "priority",
            type: "list",
            dataType: "string",
            required: true,
            values: [
                { value: "high", text: "High" },
                { value: "middle", text: "Middle" },
                { value: "low", text: "Low" }
            ],
            binding: {
                value: "value",
                text: "text"
            }
        },
        {
            name: "owner",
            type: "list",
            dataType: "integer",
            required: true,
            values: [
                { id: 3, userName: "song.zhang@leadrive.com", displayName: "张嵩" },
                { id: 57, userName: "sixue.chen@leadrive.com", displayName: "陈思雪" },
            ],
            binding: {
                value: "id",
                text: "displayName"
            }
        },
        {
            name: "owner2",
            type: "text",
            dataType: "integer",
            required: true,
        },
    ]
};
Vue.component("datalist-new", {
    props: {
        title: {
            type: String,
            default: "Apply a New Item"
        },
    },
    data: function () {
        return {
            table: null,
        };
    },
    template: `
    <div class="alert bg-white shadow">
        <p class="font-weight-bold">{{title}}</p>
        <hr />
        <div v-if="table==null">fdsf</div>
        <div v-if="table!=null">
            <div v-for="field in table.fields" class="form-group row">
                <label :for="field.name+'Input'" class="col-sm-2 col-form-label text-sm-right">
                    {{getFieldTitle(field)}}
                    <template v-if="isFieldRequired(field)"><span class="text-danger">*</span></template>
                </label>
                <div class="col-sm-10">
                    <template v-if="isFieldShowAsText(field)">
                        <input type="text" class="form-control" :id="field.name+'Input'" v-model="table.data[field.name]" />
                    </template>
                    <template v-if="isFieldShowAsTextArea(field)">
                        <textarea class="form-control" :id="field.name+'Input'" rows="4" v-model="table.data[field.name]" ></textarea>
                    </template>
                    <template v-if="isFieldShowAsSelect(field)">
                        <select class="custom-select" :id="field.name+'Input'" v-model="table.data[field.name]" >
                            <option v-for="value in field.values" :value="getFieldListItemValue(field, value)">{{getFieldListItemText(field,value)}}</option>
                        </select>
                    </template>
                </div>
            </div>
            <div>{{table.data["title"]}}</div>
            <div class="form-group row">
                <label class="col-sm-2 col-form-label text-sm-right"></label>
                <div class="col-sm-10">
                    <button class="btn btn-primary" @click="submit">New</button>
                </div>
            </div>
        </div>
    </div>
    `,
    mounted: function () {
        console.info("mounted");
        let table = tableDef;
        table.data = {};
        table.oldData = {};
        for (let field of table.fields.values()) {
            if (field.dataType == "string") {
                if ("defaultValue" in field) {
                    table.data[field.name] = String(field.defaultValue);
                    table.oldData[field.name] = String(field.defaultValue);
                } else {
                    table.data[field.name] = "";
                    table.oldData[field.name] = "";
                }
            } else if (field.dataType == "integer" || field.dataType == "float") {
                if ("defaultValue" in field) {
                    table.data[field.name] = Number(field.defaultValue);
                    table.oldData[field.name] = Number(field.defaultValue);
                }
                else {
                    table.data[field.name] = 0;
                    table.oldData[field.name] = 0;
                }
            }
            else if (field.dataType == "bool") {
                if ("defaultValue" in field) {
                    table.data[field.name] = Boolean(field.defaultValue);
                    table.oldData[field.name] = Boolean(field.defaultValue);
                }
                else {
                    table.data[field.name] = false;
                    table.oldData[field.name] = false;
                }
            }

        }
        this.table = table;
        for (let field of table.fields.values()) {
            //Vue.set(table.data, field.name, "");
        }
        for (let field of table.fields.values()) {
            try {
                if (field.type == "list") {
                    if ("values" in field) {
                        // keep the values
                    }
                    else if ("dataSource" in field) {
                        Vue.set(field, "values", []);
                        this.getFieldListValues(field.name);
                    }
                    else {
                        Vue.set(field, "values", []);
                        field.values = [];
                    }
                }
            }
            catch (error) { }
        }
        console.info("end of mounted");
    },
    methods: {
        getFieldListValues: function (fieldName) {
            console.info("getFieldListValues: " + fieldName);
            let field = this.table.fields.find(function (item) {
                return item.name == fieldName;
            });
            if (field == undefined) return;
            let dataSource = field.dataSource;
            let url = dataSource.url;
            let inputData = { filters: {} };
            for (let item of dataSource.filters) {
                if (item in this.table.data) {
                    if (this.table.data[item] != "") {
                        inputData.filters[item] = this.table.data[item];
                    }
                    else {
                        inputData.filters[item] = "";
                    }
                }
            }
            $.ajax({
                type: "POST",
                url: url,
                contentType: "application/json",
                data: JSON.stringify(inputData),
                dataType: "json",
                async: true,
                context: this,
                beforeSend: function () {
                    console.info("getFieldListValues_beforeSend: " + fieldName);
                    field.values = [];
                },
                success: function (rsp) {
                    console.info("getFieldListValues_successCallback: " + fieldName);
                    if (!rsp.isSuccess) {
                        field.values = []; return;
                    }
                    field.values = rsp.result;
                    console.log(rsp);
                },
                error: null,
                complete: null,
            });
        },
        isFieldRequired: function (field) {
            if ("required" in field) return field.required; else return false;
        },
        getFieldTitle: function (field) {
            if (!("title" in field)) return field.name; else return field.title;
        },
        isFieldShowAsText: function (field) {
            return field.type == "text";
        },
        isFieldShowAsTextArea: function (field) {
            return field.type == "textarea";
        },
        isFieldShowAsSelect: function (field) {
            return field.type == "list";
        },
        getFieldListItemValue: function (field, item) {
            try {
                return item[field.binding.value];
            }
            catch (e) {
                return item;
            }
        },
        getFieldListItemText: function (field, item) {
            try {
                return item[field.binding.text];
            }
            catch (e) {
                return item;
            }
        },
        submit: function () {
            console.info("Submit...");
            let inputData = { function: "new", parameters: {} };
            for (let field of this.table.fields) {
                inputData.parameters[field.name] = this.table.data[field.name];
            }

            $.ajax({
                type: "POST",
                url: this.table.url,
                contentType: "application/json",
                data: JSON.stringify(inputData),
                dataType: "json",
                async: true,
                context: this,
                beforeSend: function () {
                    console.info("submit_beforeSend");
                },
                success: function (rsp) {
                    console.info("submit_successCallback");
                    if (!rsp.isSuccess) {
                        return;
                    }
                    console.log(rsp);
                },
                error: null,
                complete: null,
            });
        }
    },
    watch: {
        table: {
            handler: function (newVal) {
                if (this.table === null || this.table === undefined) return;
                for (let field of this.table.fields) {
                    if (this.table.data[field.name] != this.table.oldData[field.name]) {
                        console.log(field.name + " changed");
                        for (let field2 of this.table.fields) {
                            try {
                                if ((field2.type == "list") && ("dataSource" in field2)) {
                                    if (field2.dataSource.filters.includes(field.name)) {
                                        console.log("update " + field2.name);
                                        this.getFieldListValues(field2.name);
                                    }
                                }
                            }
                            catch (e) { }
                        }
                        this.table.oldData[field.name] = this.table.data[field.name]
                    }
                }
            },
            deep: true,
            immediate: true,
        }
    }
});
