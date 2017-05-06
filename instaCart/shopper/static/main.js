/**
 * Created by asmita on 5/5/17.
 */
var email;  var lastname; var firstname; var cityName; var statename;
function validateEmail() {
    var x = document.getElementById("email").value;
    var fname = document.getElementById("fname").value;
    var lname = document.getElementById("lname").value;
    var city = document.getElementById("city").value;
    var state = document.getElementById("state").value;
    var atpos = x.indexOf("@");
    var dotpos = x.lastIndexOf(".");
    if(fname.length < 1){
        alert("first name is required");
    }else if(lname.length <1){
        alert("last name is required");
    }else if(city.length <1){
        alert("city is required");
    }else if(state.length <1){
        alert("state is required");
    }else if (atpos<1 || dotpos<atpos+2 || dotpos+2>=x.length) {
        alert("Not a valid e-mail address");
        return false;
    }else{
        email = x;
        lastname=lname;
        firstname=fname;
        cityName= city;
        statename= state;
        var ele = document.getElementById("continue");
        ele.setAttribute("data-toggle","modal");
        ele.setAttribute("data-target","#agreementModal");
        ele.setAttribute("data-dismiss","modal");
        //console.log(email);
    }

}

function addAttribute(){
    var form = document.getElementById("form");
    var x = document.createElement("INPUT");
    x.setAttribute("type", "hidden");
    x.setAttribute("name","first_name");
    x.setAttribute("value", firstname);
    form.appendChild(x);

    var input2 = document.createElement("INPUT");
    input2.setAttribute("type", "hidden");
    input2.setAttribute("name","last_name");
    input2.setAttribute("value", lastname);
    form.appendChild(input2);


    var emailInput = document.createElement("INPUT");
    emailInput.setAttribute("type", "hidden");
    emailInput.setAttribute("name","email");
    emailInput.setAttribute("value", email);
    form.appendChild(emailInput);

    var cityinput = document.createElement("INPUT");
    cityinput.setAttribute("type", "hidden");
    cityinput.setAttribute("name","city");
    cityinput.setAttribute("value", cityName);
    form.appendChild(cityinput);

    var stateInput = document.createElement("INPUT");
    stateInput.setAttribute("type", "hidden");
    stateInput.setAttribute("name","state");
    stateInput.setAttribute("value", statename);
    form.appendChild(stateInput);


    console.log(x);
}


