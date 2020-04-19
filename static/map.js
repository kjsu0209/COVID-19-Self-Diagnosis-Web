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
              html_str = html_str + "<h6>" + s_list[i] + "</h6><input id='" + s_list[i] + "' type=\"text\" name=\"daterange\" value=\"04/17/2020 - 04/20/2020\" /><hr>";
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
        symptoms = symptoms + symptoms_result[i].innerText + ',';
    }

  let r = document.getElementById("RAD_result");

    // Result ( Green = 0, Yellow = 1, Red = 2 )
    var alert_num = [0, 0, 0]
    var alert_img = [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Green_Light_Icon.svg/348px-Green_Light_Icon.svg.png',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Yellow_Light_Icon.svg/348px-Yellow_Light_Icon.svg.png',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Red_Light_Icon.svg/348px-Red_Light_Icon.svg.png'
    ]

  //Simplified XMLHttpRequest supported by all browsers except IE11
   var get_url = 'http://127.0.0.1:5000/step3?symptom=' + symptoms;
  fetch(get_url)
      .then((response)=>response.json())
      .then((datas)=>{
          // Get result A - symptom
          var str = '';
          var d= datas['rad'].toString();
          var data = JSON.parse(d);
          var keys = Object.keys(data);
          var count = 0, rad_sum = 0, symptom_count = 0;
          for(var k = 0; k< keys.length; k++){
              var key = keys[k];
              str = str + key + ' : ';
              if(data[key] == 0){
                  str = str + 'Not COVID-19 symptom';
              }
              else if(data[key] == 1){
                    str = str + 'Common COVID-19 symptom';
                  symptom_count += 1;
              }
              else{
                    str = str + 'COVID-19 symptom with RAD value : ';
                    rad_sum += data[key];
                    count += 1;
                    symptom_count += 1;
                    if(data[key] > 0.4){
                        str = str + 'High';
                    }
                    else if(data[key]<0.3){
                        str = str + 'Low';
                    }
                    else{
                        str = str + 'Moderate';
                    }
              }
              str = str + '<hr>'
          }
          r.innerHTML = str;

          if(rad_sum == 0 && symptom_count == 0){
              alert_num[0] = 0;
          }
          else if(rad_sum/count > 0.3 || k >= 3){
              alert_num[0] = 2;
          }
          else{
              alert_num[0] = 1;
          }


          // Get result B - period of symptom
          var earier_start = new Date();
          var later_end = new Date();
          let datebox = document.getElementsByName('daterange')
            var date;
          for(var a=0;a < datebox.length;a++){
              date = datebox[a];
              var date_string = date.value
              var date_arry = date_string.split(' - ');
              var start = date_arry[0].replace('/', '-');
              var end = date_arry[1].replace('/', '-');
             var start_date = new Date(start);
             var end_date = new Date(end);
             if(start_date < earier_start) earier_start = start_date;
             if(end_date < later_end) later_end = end_date;
          }
            var today = new Date();
                        console.log(later_end - earier_start)
          if(later_end >= today){
              if(later_end - earier_start >= 14){
                  alert_num[1] = 2;
              }
              else if (later_end - earier_start <= 7){
                  alert_num[1] = 1;
              }
              else{
                  alert_num[1] = 2;
              }
          }
          else{
                if (today - earier_start <= 7){
                    alert_num[1] = 1;
                }
                else if(later_end - earier_start < 5){
                    alert_num[1] = 1;
                }
                else {
                    alert_num[1] = 0;
                }
          }


          // Get result C - questions
          let checkbox = []
          checkbox[0] = document.getElementById('defaultCheck1').checked;
          checkbox[1] = document.getElementById('defaultCheck2').checked;
          checkbox[2] = document.getElementById('defaultCheck3').checked;
          var checknum = 0;
          for (var a =0;a<3;a++){
              if(checkbox[a] == true){
                  checknum += 1;
              }
          }
          alert_num[2] = checknum;

            //Set result images
          var images = []
          images[0] = document.getElementById("alert_img_A");
          images[1] = document.getElementById("alert_img_B");
          images[2] = document.getElementById("alert_img_C");
          for(a=0;a<3;a++){
              images[a].src = alert_img[alert_num[a]];
          }
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