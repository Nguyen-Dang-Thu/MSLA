window.onload = function () {
	var dataPoints1 = [];
	for (x in jArray_attack) {
	    dataPoints1.push({
		y: jArray_attack[x]["number"],
		label: Math.round(jArray_attack[x]["number"] / total * 100)  + "%",
		indexLabel: jArray_attack[x]["name"]
	    });
	}
	var chart1 = new CanvasJS.Chart("attackChart", {
	    title: {
		text: "Messenger",
		fontFamily: "Verdana",
		fontColor: "Peru",
		fontSize: 28

	    },
	    axisY: {
		tickThickness: 0,
		lineThickness: 0,
		valueFormatString: " ",
		gridThickness: 0
	    },
	    axisX: {
		tickThickness: 0,
		lineThickness: 0,
		labelFontSize: 18,
		labelFontColor: "Peru"

	    },
	    data: [{
		indexLabelFontSize: 14,
		toolTipContent: "<span style='\"'color: {color};'\"'><strong>{indexLabel}</strong></span><span style='\"'font-size: 24px; color:peru '\"'><strong>{y}</strong></span>",
		indexLabelPlacement: "outside",
		indexLabelFontColor: "black",
		indexLabelFontWeight: 600,
		indexLabelFontFamily: "Verdana",
		color: "#62C9C3",
		type: "bar",
		dataPoints: dataPoints1
	    }]
	});

	chart1.render();

        var dataPoints2 = [];
        for (x in jArray_os) {
            dataPoints2.push({
                y: jArray_os[x]["number"],
                legendText: jArray_os[x]["name"],
                label: Math.round(jArray_os[x]["number"] / total *100) + "%"
            });
        }
        var chart2 = new CanvasJS.Chart("osChart", {
            title: {
                text: "OS Analysis"
            },
            legend: {
                verticalAlign: "center",
                horizontalAlign: "left",
                fontSize: 20,
                fontFamily: "Helvetica"
            },
            theme: "theme3",
            data: [{
                type: "pie",
                indexLabelFontFamily: "Garamond",
                indexLabelFontSize: 20,
                startAngle: -20,
                showInLegend: true,
                toolTipContent: "{label}",
                dataPoints: dataPoints2
            }]
        });

        chart2.render();

	function getMonthFromString(mon) {
            return new Date(Date.parse(mon + " 1, 2012")).getMonth() + 1
        }
        var dataPoints3 = [];
        var result = [];
        var max_value = 0;
        result = jArray_date[0]["name"].split("/");
        result[1] = getMonthFromString(result[1]);
        var date_start = new Date(result[2], result[1], result[0]);
        for (x in jArray_date) {
            if (jArray_date[x]["number"] > max_value) {
                max_value = jArray_date[x]["number"];
            }
            result = jArray_date[x]["name"].split("/");
            result[1] = getMonthFromString(result[1]);
            dataPoints3.push({
                x: new Date(result[2], result[1], result[0]),
                y: jArray_date[x]["number"]
            });
        }
        var chart3= new CanvasJS.Chart("dateChart", {
            title: {
                text: "Attack per day"
            },
            axisX: {
                valueFormatString: "DD-MMM",
                interval: 10,
                intervalType: "day",
                labelAngle: -50,
                labelFontColor: "rgb(0,75,141)",
                minimum: date_start
            },
            axisY: {
                title: "Attack",
                interlacedColor: "#F0FFFF",
                tickColor: "azure",
                titleFontColor: "rgb(0,75,141)",
                valueFormatString: "#",
                interval: max_value / 2
            },
            data: [{
                indexLabelFontColor: "darkSlateGray",
                name: 'views',
                type: "area",
                color: "rgba(0,75,141,0.7)",
                markerSize: 8,
                dataPoints: dataPoints3
            }

            ]
        });

        chart3.render();

        var dataPoints4 = [];
        for (x in jArray_browser) {
            dataPoints4.push({
                y: jArray_browser[x]["number"],
                label: jArray_browser[x]["name"]
            });
        }

	CanvasJS.addColorSet("greenShades",
                [//colorSet Array

                "#2F4F4F",
                "#008080",
                "#2E8B57",
                "#3CB371",
                "#90EE90"                
                ]);

        var chart4 = new CanvasJS.Chart("browserChart", {
	    colorSet: "greenShades",
            title: {
                text: "Browser Analysis"
            },
            axisX: {
                title: "Browser"
            },
            axisY: {
                title: "Count"
            },

            data: [{
                type: "column",
                dataPoints: dataPoints4
            }]
        });

        chart4.render();

        var dataPoints5 = [];
        for (x in jArray_ip) {
            dataPoints5.push({
                y: jArray_ip[x]["number"],
                label: Math.round(jArray_ip[x]["number"] / total * 100) + "%",
                indexLabel: jArray_ip[x]["name"]
            });
        }
        var chart5 = new CanvasJS.Chart("ipChart", {
            title: {
                text: "IP Attack",
                fontFamily: "Verdana",
                fontColor: "Peru",
                fontSize: 28

            },
            axisY: {
                tickThickness: 0,
                lineThickness: 0,
                valueFormatString: " ",
                gridThickness: 0
            },
            axisX: {
                tickThickness: 0,
                lineThickness: 0,
                labelFontSize: 18,
                labelFontColor: "Peru"

            },
            data: [{
                indexLabelFontSize: 14,
                toolTipContent: "<span style='\"'color: {color};'\"'><strong>{indexLabel}</strong></span><span style='\"'font-size: 24px; color:peru '\"'><strong>{y}</strong></span>",
                indexLabelPlacement: "outside",
                indexLabelFontColor: "black",
                indexLabelFontWeight: 600,
                indexLabelFontFamily: "Verdana",
                color: "#62C9C3",
                type: "bar",
                dataPoints: dataPoints5
            }]
        });

        chart5.render();
}
