window.onload = function () {
	function httpGet(theUrl){
		var xmlHttp = null;
		xmlHttp = new XMLHttpRequest();
		xmlHttp.open( "GET", theUrl, false );
		xmlHttp.send( null );
		return xmlHttp.responseText;
	}

		var dataPoints1 = [];
		var dataPoints2 = [];

		var chart = new CanvasJS.Chart("chartContainer",{
			zoomEnabled: true,
			title: {
				text: "System Monitor"		
			},
			toolTip: {
				shared: true
				
			},
			legend: {
				verticalAlign: "top",
				horizontalAlign: "center",
                                fontSize: 14,
				fontWeight: "bold",
				fontFamily: "calibri",
				fontColor: "dimGrey"
			},
			axisX: {
				title: "Time"
			},
			axisY:{
				prefix: '',
				includeZero: false
			}, 
			data: [{ 
				// dataSeries1
				type: "line",
				xValueType: "dateTime",
				showInLegend: true,
				name: "CPU",
				dataPoints: dataPoints1
			},
			{				
				// dataSeries2
				type: "line",
				xValueType: "dateTime",
				showInLegend: true,
				name: "RAM" ,
				dataPoints: dataPoints2
			}],
          legend:{
            cursor:"pointer",
            itemclick : function(e) {
              if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
                e.dataSeries.visible = false;
              }
              else {
                e.dataSeries.visible = true;
              }
              chart.render();
            }
          }
		});



		var updateInterval = 3000;
		// initial value
		var yValue1 = 0; 
		var yValue2 = 0;

		var time = new Date();

		var updateChart = function (count) {
			count = count || 1;

			for (var i = 0; i < count; i++) {
				
				// add interval duration to time				
				time.setTime(time.getTime()+ updateInterval);
				
				//get cpu, ram information
				var val = httpGet("/usage").split("|")
				yValue1 = parseFloat(val[0]);
				yValue2 = parseFloat(val[1]);
				
				// pushing the new values
				dataPoints1.push({
					x: time.getTime(),
					y: yValue1
				});
				dataPoints2.push({
					x: time.getTime(),
					y: yValue2
				});
				if (dataPoints1.length >=  300 )
				{
					dataPoints1.shift();
					dataPoints2.shift();				
				}

			};

			// updating legend text with  updated with y Value 
			chart.options.data[0].legendText = " CPU " + yValue1 + "%";
			chart.options.data[1].legendText = " RAM " + yValue2 + "%"; 
			
			chart.render();

		};

		// generates first set of dataPoints 
		updateChart(1);	
		 
		// update chart after specified interval 
		setInterval(function(){updateChart()}, updateInterval);
	}
