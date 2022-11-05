/* globals Chart:false, feather:false */

(() => {
    'use strict'

    $('.service-container').each(function () {
        var container = $(this);
        var salary_of_days = container.data('salary_of_days');
        var get_massive_columns = container.data('get_massive_columns');
        const ctx = document.getElementById('myChart')
        const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: get_massive_columns,
                datasets: [{
                    data: salary_of_days,
                    lineTension: 0,
                    backgroundColor: 'transparent',
                    borderColor: '#6691be',
                    borderWidth: 4,
                    pointBackgroundColor: '#ffffff'
                }]
            },
            options: {
                tooltips: {
                    cornerRadius: 5,
                    caretSize: 0,
                    xAlign: 'right',
                    yAlign: 'top',
                    displayColors: false,
                    xPadding: 12,
                    yPadding: 10,
                    backgroundColor: '#6691be',
                    titleFontStyle: 'normal',
                    titleMarginBottom: 10,
                    callbacks: {
                        title: function (tooltipItems) {
                            return `День ${tooltipItems[0].xLabel}`
                        },
                        label: function(tooltipItems) {
                            return `${tooltipItems.yLabel} руб.`
                        }
                    }
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: false
                        }
                    }]
                },
                legend: {
                    display: false
                }
            }
        })
    });

    document.querySelector("#clickMe").onclick = function () {
        let myDate = new Date(document.getElementById('monthcalen').value);
        if (myDate.getMonth() + 1 <= 9) {
            window.location.href = `${window.location.href.slice(0, -8)}/${myDate.getFullYear()}/0${myDate.getMonth() + 1}`;
        } else {
            window.location.href = `${window.location.href.slice(0, -8)}/${myDate.getFullYear()}/${myDate.getMonth() + 1}`;
        }
    }
})()