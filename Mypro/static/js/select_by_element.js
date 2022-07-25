function add(e){
    id = $(e).attr("id");
    let table;
    let end;
    if(id == 'add1'){
        table = $("#table1");
        end = $("#contain").children("option[group='0']").last();
        group_num= 0;

    }else if(id == 'add2'){
        table  = $("#table2");
        end = $("#contain").children("option[group='1']").last();
        group_num = 1;
    }else {
        table = $("#table3");
        end = $("#contain").children("option[group='2']").last();
        group_num =2;
    }
    checks = table.find('input[name="select"]');
    list_options = [];
    global_flag = 0 ; 
    alert_text = "";
    for(var i of checks){
        if(i.checked){
            flag = 0;
            option = {};
            value = i.value;
            option['min'] = document.getElementById("min_"+value).value;
            option['max'] = document.getElementById("max_"+value).value;
            option['des'] = document.getElementById("des_"+value).innerText;
            option['unit'] = document.getElementById("unit_"+value).innerText;
            if(document.getElementById("ch_"+value).checked){
                option['nor'] = "OR";
            }else{
                option['nor'] = "AND";
            }
            if(option['min']==''||option['max']==''){
                alert_text += option['des']+"条目有空值，请输入后继续\n";
                flag=1;
                global_flag=1;
            } 
            if(flag==0){
                if(Number(option['min'])>Number(option['max'])){
                    alert_text += option['des']+"条目最小值大于最大值,请重新输入\n";
                    flag=1;
                    global_flag=1;
                }
            }
            if(flag!=1)        list_options.push(option);
        }
    }
    
    ll = []
    for(var i of list_options){
        var op = document.createElement("option");
        op.setAttribute("group",String(group_num));
        op.setAttribute("class","op");
        op.setAttribute("con","1")
        op.innerHTML='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+i['des']+': '+i['min']+' - '+i['max']+'&nbsp'+i['unit']+'&nbsp'+'('+i['nor']+')'
        ll.push(op);
    }
    for(var i = ll.length-1 ; i >=0 ; i--){
        end.after(ll[i]);
    }
    if(global_flag==1){
        alert(alert_text);
    }

}

function removeall(){
    ll = $("#contain").find("option[group='0']");
    remove_elements(ll);
    ll = $("#contain").find("option[group='1']");
    remove_elements(ll);
    ll = $("#contain").find("option[group='2']");
    remove_elements(ll);
}

function remove_elements(ll){
    // console.log(ll.first().next().text());
    // console.log(ll.length);
    let i = ll.length;
    cu =  ll.first().next();
    if(i>1){
        for(var n = 0 ; n < i-1 ; n++){
            let next = cu.next();
            cu.remove();
            cu = next;
            
        }
    }
    
    
}

function remove(){
    var contain=document.getElementById('contain');
    // console.log(contain.options[0].getAttribute("con"));
    var index =contain.selectedIndex;
    if(contain.options[index].getAttribute("con")=="1"){
        contain.options.remove(index);
    }
   
        
}


function sub(){
    var contain=document.getElementById('contain')
    data=[]
    for(i of contain.options){
        data.push(i.value.trim());
    }
    console.log(data);
}