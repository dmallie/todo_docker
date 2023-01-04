'use strict';
const displayTime = document.getElementById('cal__time');
// create a new date object
// to calculate the current time
const currentTime = () => {
       var date = new Date();
       let hour = date.getHours();
       let minute = date.getMinutes();
       let second = date.getSeconds();
       var disp_second;
       if(second < 10){
              disp_second = `0${second}`;
       }
       else{
              disp_second = `${second}`;
       }
       if (minute < 10){
              displayTime.textContent = `${hour}:0${minute}:${disp_second}`;
       }else{
              displayTime.textContent = `${hour}:${minute}:${disp_second}`;
       }
};
// call this function to update the minutes every 60 seconds
setInterval(currentTime, 1000);

currentTime();