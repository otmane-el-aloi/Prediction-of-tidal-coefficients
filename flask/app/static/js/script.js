 // get selected row
 // display selected row data in text input
 //Recuperer le tableau 
 var table = document.getElementById("dataTable");
 var rIndex;

 // pour stocker data 
 let data2 = [];
 for (var i = 1; i < table.rows.length; i++) {
     rIndex = this.rowIndex;
     var item = {

     };
     item.date = i//table.rows[i].cells[0].innerHTML
     item.min = table.rows[i].cells[1].innerHTML
     item.max = table.rows[i].cells[2].innerHTML
     console.log(item.id);
     data2.push(item);
 }
 // afficher data tu array
 console.log(data2);

 var xyValues1 = []; // pour afficher date en fonction de min 
 var xyValues2 = []; // pour afficher date en fonction de max
 for (let i = 0; i < data2.length; i++) {
     xyValues1.push({ x: data2[i].date, y: data2[i].min });
     xyValues2.push({ x: data2[i].date, y: data2[i].max });
 }


 // afficher data , min 
 new Chart("myChart", {
     type: "scatter",
     data: {
         datasets: [{
            label: 'MinCoeffVariation',
           
            backgroundColor: 'rgb(0,0,255)',
            pointRadius: 4, 
            pointBackgroundColor: "rgb(0,0,255)", 
            data: xyValues1,
            

         }]
     },
     options: {
         legend: { display: true },
         scales: {
             xAxes: [{ ticks: { min: 0, max: 20 } }],
             yAxes: [{ ticks: { min: 0, max: 130} }],
         }
     }
 });
 // afficher data , min 
 new Chart("myChartMax", {
     type: "scatter",
     data: {
         datasets: [{
             pointRadius: 4,
             label: 'MaxCoeffVariation',
             backgroundColor: 'rgb(255, 99, 132)',
             pointBackgroundColor: "rgb(255, 99, 132)",
             data: xyValues2,

         }]
     },
     options: {
         legend: { display: true },
         scales: {
             xAxes: [{ ticks: { min: 0, max: 20 } }],
             yAxes: [{ ticks: { min: 0, max: 130} }],
         }
     }
 });