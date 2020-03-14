var qmsFileviewer=Vue.component("qms-fileviewer",{
    template:`
    <div class="d-flex flex-column">
        <div></div>
        <div class="flex-fill overflow-auto">

        </div>
    </div>
    `,
    props:['content'],
    data:function(){
        return {
            parseResult:null,
        }
    },
    computed:{

    },
    watch:{
        content:function(){
            let rows = this.content.split("\n");
            let nodes=[];
            let chapters=[];    // h1
            let chapter=null;
            let sections=[];    // h2
            let section=null;
            let articals=[];    // h3
            let artical=null;
            let tokenBuf=[];
            for(let i = 0, len = rows.length; i < len; i++){
                let row=rows[i];
                let node=this.parseLine(row, true);
            }
        }
    },
    methods:{
        parse:function(text){
            let rows = initStr.split("\n");
            let nodes=[];
            let html="";
           
            return html;
        },
        parseLine:function(text, lineStart){
            let node=null;
            if(row.match(/^#\s/)){              // h1, chapter
                node=({ type: "h1", value: this.formatLine(rows[i].substring(2)),});
            }
            else if(row.match(/^##\s/)){        // h2, section
                node=({ type: "h2", value: this.formatLine(rows[i].substring(3)),});
            }
            else if(row.match(/^###\s/)){       // h3, artical
                node=({ type: "h3", value: this.formatLine(rows[i].substring(4)),});
            }
            else if(row.match(/^####\s/)){      // h4, clause
                node=({ type: "h4", value: this.formatLine(rows[i].substring(5)),});
            }
            else if(row.match(/^#####\s/)){     // h5,
                node=({ type: "h5", value: this.formatLine(rows[i].substring(6)),});
            }
            else if(row.match(/^######\s/)){    // h6
                node=({ type: "h6", value: this.formatLine(rows[i].substring(7)),});
            }
            else if(row.match(/^\s*\*\s/)){     // ul
                let wsCount=row.match(/^\s*\s/).length;

            }
            else if(row.match(/^\d\.\s/)){      // ol

            }
            return node;
        }
    }

});

class Markdown{
    static h1Parse(text){
        if (typeof text!=="string"){
            return null;
        }
        if(text.match(/^#\s/)){
            return {

            }
        }
        return null;
    }
    static parse(initStr){
        
    }
    static formatLine(text){
        return text;
    }
    static format (str) {
        str = str.replace(/\s/g, '&nbsp;');

        var bold = str.match(/\*{2}[^*].*?\*{2}/g); // 惰性匹配
        if (bold) {
            for (var i = 0, len = bold.length; i < len; i++) {
                str = str.replace(bold[i], '<b>' + bold[i].substring(2, bold[i].length - 2) + '</b>');
            }
        }

        var italic = str.match(/\*[^*].*?\*/g);
        if (italic) {
            for (i = 0, len = italic.length; i < len; i++) {
                str = str.replace(italic[i], '<i>' + italic[i].substring(1, italic[i].length - 1) + '</i>');
            }
        }

        var code = str.match(/`.+`/g);
        if (code) {
            for (i = 0, len = code.length; i < len; i++) {
                str = str.replace(code[i], '<code>' + code[i].substring(1, code[i].length - 1) + '</code>');
            }
        }

        var img = str.match(/!\[.*\]\(.*\)/g);
        var re1 = /\(.*\)/;
        var re2 = /\[.*\]/;
        if (img) {
            for (i = 0, len = img.length; i < len; i++) {
                var url = img[i].match(re1)[0];
                var title = img[i].match(re2)[0];
                str = str.replace(img[i], '<img src=' + url.substring(1, url.length - 1) + ' alt=' + title.substring(1, title.length - 1) + '>');
            }
        }

        var a = str.match(/\[.*\]\(.*\)/g);
        if (a) {
            for (i = 0, len = a.length; i < len; i++) {
                var url = a[i].match(re1)[0];
                var title = a[i].match(re2)[0];
                str = str.replace(a[i], '<a href=' + url.substring(1, url.length - 1) + '>' + title.substring(1, title.length - 1) + '</a>');
            }
        }

        return str;
    }
}