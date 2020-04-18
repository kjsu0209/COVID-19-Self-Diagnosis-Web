function step1(){
  let list = document.getElementById("symptom_list");
  // show step 2
  let s = document.getElementById("step2");

  let s_datepicker = document.getElementById("symptomPeriod");

  let symptom = document.getElementById("step1_input").value;

  //Simplified XMLHttpRequest supported by all browsers except IE11
    var get_url = 'http://127.0.0.1:5000/step1?symptom=' + symptom;
  fetch(get_url)
      .then((response)=>response.json())
      .then((data)=>{
          var s_list = data['symptoms'].toString().split(',');
          var html_str = "";
          for(var i in s_list){
              html_str = html_str + "<div class='btn btn-success btn-symptom'>" + s_list[i] + "</div>"
          }
          list.innerHTML = html_str;

          // distribute datepicker to each symptoms
          html_str = "";
          for(var i in s_list){
              html_str = html_str + "<h6>" + s_list[i] + "</h6><input type=\"text\" name=\"daterange\" value=\"04/17/2020 - 04/20/2020\" /><hr>";
          }
          s_datepicker.innerHTML = html_str;
          daterangejquery();
          // show step2 box
          s.style.display = "block";

      })
      .catch(err =>{
          alert("Error : " + err);
      })
}
$(function() {
    daterangejquery = function(){
         $('input[name="daterange"]').daterangepicker({
            opens: 'left'
          }, function(start, end, label) {
            console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
          });
    }

});
function step2(){
  // show step 3
  s = document.getElementById("step3");
  s.style.display = "block";
}

function step3(){
  // show result
  s = document.getElementById("result");
  s.style.display = "block";

  var symptoms = ''
  let symptoms_result = document.getElementsByClassName("btn-symptom")

    for (var i=0;i<symptoms_result.length;i++){
        console.log(symptoms_result[i].innerText)
        symptoms = symptoms + symptoms_result[i].innerText + ',';
    }

  let r = document.getElementById("RAD_result");

  //Simplified XMLHttpRequest supported by all browsers except IE11
   var get_url = 'http://127.0.0.1:5000/step3?symptom=' + symptoms;
  fetch(get_url)
      .then((response)=>response.json())
      .then((data)=>{
          r.innerHTML = data['rad'].toString();
      })
      .catch(err =>{
          alert("Error : " + err);
      })
}

function addPlace(){
  //add place
  s = document.getElementById("step3");
  v = document.getElementById("visited");
  placenum += 1;
  v.innerHTML = v.innerHTML + "<input class=\"form-control\" type=\"text\" placeholder=\"Stephen's Green\" id='p" + placenum + "'>\n";
}