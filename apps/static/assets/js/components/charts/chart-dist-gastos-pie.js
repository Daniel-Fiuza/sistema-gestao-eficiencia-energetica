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
				labels: 'labels' in data_dist_gastos !== undefined ? data_dist_gastos['labels'] : [],
				datasets: 'datasets' in data_dist_gastos !== undefined ? data_dist_gastos['datasets'] : [],
			},
			options: {
				maintainAspectRatio: false,
				tooltips: {
					enabled: true,
					mode: 'single',
					callbacks: {
						label: function(tooltipItems, data) {
							return data.labels[tooltipItems.index] + ': ' + data.datasets[0].data[tooltipItems.index] + ' %';
						}
					}
				},
				plugins: {
					colorschemes: {
					  scheme: 'brewer.DarkTwo8'
					}
				}
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
