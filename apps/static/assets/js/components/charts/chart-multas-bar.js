//
// Bars chart
//

var MultasBar = (function() {

	//
	// Variables
	//

	var $chart = $('#multas-bar');


	//
	// Methods
	//

	// Init chart
	function initChart($chart) {

		// Create chart
		var ordersChart = new Chart($chart, {
			type: 'bar',
			data: {
				labels: 'labels' in data_multas !== undefined ? data_multas['labels'] : [],
				datasets: 'datasets' in data_multas !== undefined ? data_multas['datasets'] : [],
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
