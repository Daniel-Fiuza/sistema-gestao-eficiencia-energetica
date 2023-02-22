//
// Bars chart
//

var KwhEfetivoBar = (function() {

	//
	// Variables
	//

	var $chart = $('#kwh-efetivo-bar');


	//
	// Methods
	//

	// Init chart
	function initChart($chart) {

		// Create chart
		var ordersChart = new Chart($chart, {
			type: 'bar',
			data: {
				labels: 'labels' in data_kwh_efetivo !== undefined ? data_kwh_efetivo['labels'] : [],
				datasets: 'datasets' in data_kwh_efetivo !== undefined ? data_kwh_efetivo['datasets'] : [],
			},
			options: {
				maintainAspectRatio: true,
				scales: {
					yAxes: [{
						display: true,
						ticks: {
							beginAtZero: true
						}
					}]
				},
				tooltips: {
					enabled: true,
					mode: 'single',
					callbacks: {
						label: function(tooltipItems, data) {
							return data.datasets[0].label + ': ' + data.datasets[0].data[tooltipItems.index] + ' R$/KWh';
						}
					}
				},
			},
		});

		// Save to jQuery object
		$chart.data('chart', ordersChart);
	}


	// Init chart
	if ($chart.length) {
		initChart($chart);
	}

})();
