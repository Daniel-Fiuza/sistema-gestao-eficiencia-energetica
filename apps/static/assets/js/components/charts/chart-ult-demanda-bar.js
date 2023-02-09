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
				labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
				datasets: [{
					label: 'Demanda',
					data: [25, 20, 30, 22, 17, 29],
					borderColor: '#cc65fe',
      				backgroundColor: '#cc65fe',
				}]
			},
			options: {
				maintainAspectRatio: false,
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
