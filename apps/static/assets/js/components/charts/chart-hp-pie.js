//
// Bars chart
//

var HpPie = (function() {

	//
	// Variables
	//

	var $chart = $('#hp-pie');


	//
	// Methods
	//

	// Init chart
	function initChart($chart) {

		// Create chart
		var ordersChart = new Chart($chart, {
			type: 'pie',
			data: {
				labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
				datasets: [{
					label: 'Sales',
					data: [25, 20, 30, 22, 17, 29],
					backgroundColor: ["red", "blue", "green", "yellow", "purple", "orange"], 
				}]
			},
			options: {
				maintainAspectRatio: false,
			}
		});

		// Save to jQuery object
		$chart.data('chart', ordersChart);
	}


	// Init chart
	if ($chart.length) {
		initChart($chart);
	}

})();
