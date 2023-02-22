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
				labels: 'labels' in data_hp_hfp !== undefined ? data_hp_hfp['labels'] : [],
				datasets: 'datasets' in data_hp_hfp !== undefined ? data_hp_hfp['datasets'] : []
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
					  scheme: 'office.Austin6'
					//   scheme: 'brewer.SetOne9'
					}
				},
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
