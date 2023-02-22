//
// Bars chart
//

var UltDemandaBar = (function() {

	//
	// Variables
	//

	var $chart = $('#ult-demanda-bar');


	//
	// Methods
	//

	// Init chart
	function initChart($chart) {

		// Create chart
		var ultDemandaBar = new Chart($chart, {
			type: 'bar',
			data: {
				labels: 'labels' in data_ult_demanda !== undefined ? data_ult_demanda['labels'] : [],
				datasets: 'datasets' in data_ult_demanda !== undefined ? data_ult_demanda['datasets'] : [],
			},
			options: {
				maintainAspectRatio: false,
				scales: {
					yAxes: [{
						display: true,
						ticks: {
							beginAtZero: true
						}
					}]
				}
			}
		});

		// Save to jQuery object
		$chart.data('chart', ultDemandaBar);
	}


	// Init chart
	if ($chart.length) {
		initChart($chart);
	}

})();
