/* globals Chart:false, feather:false */
var auctions = JSON.parse(document.getElementById("auctions").textContent);
console.log("auctions ==>>", auctions);

function renderCart(data, labels) {
	feather.replace();

	// Graphs
	var ctx = document.getElementById("myChart");
	// eslint-disable-next-line no-unused-vars
	var chartOne = new Chart(ctx, {
		type: "line",
		data: {
			// labels: [
			// 	"Sunday",
			// 	"Monday",
			// 	"Tuesday",
			// 	"Wednesday",
			// 	"Thursday",
			// 	"Friday",
			// 	"Saturday",
			// ],
			labels: labels,
			datasets: [
				{
					// data: [15339, 21345, 18483, 24003, 23489, 24092, 12034],
					label: "Added Count",
					data: data,
					lineTension: 0,
					backgroundColor: "transparent",
					borderColor: "#007bff",
					borderWidth: 4,
					pointBackgroundColor: "#007bff",
				},
			],
		},
		options: {
			scales: {
				yAxes: [
					{
						ticks: {
							beginAtZero: true,
						},
					},
				],
			},
			legend: {
				display: false,
			},
		},
	});
}
// renderCart();

function get_datas() {
	let data = [];
	let labels = [];
	for (let index = 0; index < auctions.length; index++) {
		data.push(auctions[index].created_count);
		labels.push(new Date(auctions[index].date).toLocaleDateString());
	}

	console.log(data, labels);

	renderCart(data, labels);
}
get_datas();
