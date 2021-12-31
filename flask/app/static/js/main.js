function initMap() {
    const myLatLng = { lat: -25.363, lng: 131.044 };
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 4,
      center: myLatLng,
    });
  
    new google.maps.Marker({
      position: myLatLng,
      map,
      title: "Hello World!",
    });
  }
  
  $(document).ready( function () {
    $('#example').dataTable( {
        "sDom": 'T<"clear">lfrtip',
        "oTableTools": {
            "sSwfPath": "/swf/copy_cvs_xls_pdf.swf"
        }
    } );
} );

  $(function() {
  $("#exporttable").click(function(e){
  var table = $("#dataTable");
  if(table && table.length){
  $(table).table2excel({
  exclude: ".noExl",
  name: "Excel Document Name",
  filename: "BBBootstrap" + new Date().toISOString().replace(/[\-\:\.]/g, "") + ".xls",
  fileext: ".xls",
  exclude_img: true,
  exclude_links: true,
  exclude_inputs: true,
  preserveColors: false
  });
  }
  });
    
    });