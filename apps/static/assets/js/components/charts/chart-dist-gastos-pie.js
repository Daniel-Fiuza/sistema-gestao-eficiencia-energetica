//
// Bars chart
//

var DistGastosPie = (function() {

	//
	// Variables
	//

	var $chart = $('#dist-gastos-pie');


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
					backgroundColor: ["#ff6384", "#36a2eb", "#cc65fe", "#ffce56", "green", "brown"], 
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
