let activeCharts = [];

function destroyExistingCharts() {
    activeCharts.forEach(chart => chart.destroy());
    activeCharts = [];
}

function drawHistogram(ctx, labels, positiveCounts, negativeCounts, scale = 'linear') {
    const data = {
        labels,
        datasets: [
            {
                label: '正の頻度',
                data: positiveCounts,
                backgroundColor: 'blue',
            },
            {
                label: '負の頻度',
                data:
                    scale === 'sqrt'
                        ? negativeCounts.map(value => -Math.sqrt(value))
                        : negativeCounts.map(value => -value),
                backgroundColor: 'red',
            },
        ],
    };

    const options = {
        scales: {
            x: {
                title: {
                    display: true,
                    text: '値の範囲',
                },
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: '頻度',
                },
            },
        },
        plugins: {
            legend: {
                display: true,
            },
        },
        maintainAspectRatio: false,
        elements: {
            bar: {
                barPercentage: 1.0,
                categoryPercentage: 1.0,
            },
        },
    };

    const chart = new Chart(ctx, { type: 'bar', data, options });
    activeCharts.push(chart);
}


// 新しい関数をグローバルスコープに公開
window.drawLogSqrtHistogram = drawLogSqrtHistogram;


// 関数をグローバルスコープに公開
window.destroyExistingCharts = destroyExistingCharts;
window.drawHistogram = drawHistogram;