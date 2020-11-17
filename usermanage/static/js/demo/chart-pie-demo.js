// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito','-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var getServerCount = function () {
    $.ajax({
        url: "/performanceTest/getServerCount/",
        type: "GET",
        async: true,
        success: function (resp) {
            if (resp.returncode === 200) {
                serverdata = resp.data;
                //console.log(serverdata);
                setData(serverdata);
                return serverdata
            } else {
                serverdata = [1, 1, 1];
                setData(serverdata);
                return serverdata;
            }
        }
    })
};
var serverdata = getServerCount();
//console.log(serverdata);


function setData(serverdata) {
    var ctx = document.getElementById("myPieChart");
    var myPieChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ["华为云", "腾讯云", "阿里云"],
            datasets: [{
                data: serverdata,
                backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
                hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
                hoverBorderColor: "rgba(234, 236, 244, 1)",
            }],
        },
        options: {
            maintainAspectRatio: false,
            tooltips: {
                backgroundColor: "rgb(255,255,255)",
                bodyFontColor: "#858796",
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: false,
                caretPadding: 10,
            },
            legend: {
                display: false
            },
            cutoutPercentage: 80,
        },
    });

}