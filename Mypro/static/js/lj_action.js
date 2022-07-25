/*
 * @Author: liujun1173727203 1173727203@qq.com
 * @Date: 2022-06-14 10:44:25
 * @LastEditors: liujun1173727203 1173727203@qq.com
 * @LastEditTime: 2022-07-01 14:22:39
 * @FilePath: \web-workplace\第一次\js\lj_action.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */

// $(document).ready(function(){
//     let login_status = sessionStorage.getItem("log_status");
// if (login_status==null){
//     sessionStorage.setItem("log_status","0");
//     login_status = "0"
// }
// console.log(login_status)
// if(login_status!="0"){
//     document.getElementById("login_name").innerText  = login_status;
// }
//
//
// })





Optiondata=[]
function add(){
    console.log('add')
    Optiondata=[]
    checks=document.getElementsByName('select')
    for(var i of checks){
        selectedtip={}
        if(i.checked){
            j=i.value
            minval =document.getElementById('min_'+j).value
            maxval =document.getElementById('max_'+j).value

            if(minval.length==0){
                alert(lists[j]+'的最小值为空值')
                return
            }
            if(maxval.length==0){
                alert(lists[j]+'的最大值为空值')
                return
            }
            selectedtip['minval']=minval
            selectedtip['name']=lists[j]
            selectedtip['maxval']=maxval
            selectedtip['unit']=units[j]
            flag=document.getElementsByName('check')[j]
            if(flag.checked){
                selectedtip['state']='OR'
            }else{
            selectedtip['state']='AND'
            }
            Optiondata.push(selectedtip)
        }
    }
    if(Optiondata.length==0){
        alert("选择为空")
        return
    }
    var select_contain=document.getElementById('contain')
    for(var i of Optiondata){
        var option =document.createElement('option')
        option.setAttribute('class','op')
        option.innerHTML='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+i.name+': '+i.minval+' - '+i.maxval+'&nbsp'+i.unit+'&nbsp'+' ('+i.state+')'
        select_contain.appendChild(option)   
    }
}

function removeall(){
    var contain=document.getElementById('contain')
    contain.options.length=1
    Optiondata=[]
}

function remove(){
    var contain=document.getElementById('contain')
        var index =contain.selectedIndex
        contain.options.remove(index)
        console.log(index);
}

function sub(){
    var contain=document.getElementById('contain')
    data=[]
    data_txt=''
    for(i of contain.options){
        data.push(i.value.trim());
        data_txt=data_txt+' '+i.value.trim();
    }
    console.log(data);
    console.log(data_txt)
    sessionStorage.setItem("sra_value",data);
    sessionStorage.setItem("sra_txt",data_txt);
    window.location.href='/user/by_sra'
}