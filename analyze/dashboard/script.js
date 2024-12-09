document.getElementById('plotButton').addEventListener('click', () => {
    destroyExistingCharts();

    const input = document.getElementById('signalInput').value.trim();
    const tValueInput = document.getElementById('tValueInput').value.trim();
    const binWidthInput = document.getElementById('binWidthInput').value.trim();
    const signalData = JSON.parse(input);

    let T = parseFloat(tValueInput);
    if (isNaN(T)) {
        const durations = [];
        for (let i = 2; i < signalData.length - 2; i += 2) {
            durations.push(signalData[i]);
        }
        T = Math.min(...durations);
        document.getElementById('tValueInput').value = T.toFixed(2);
    }

    const binWidth = parseFloat(binWidthInput) || 20;

    // 信号データを描画
    const labels = [];
    const data = [];
    let time = 0;
    for (let i = 0; i < signalData.length; i++) {
        const duration = Math.abs(signalData[i]);
        const state = signalData[i] > 0 ? 1 : 0;

        labels.push(time);
        data.push(state);

        time += duration;
        labels.push(time);
        data.push(state);
    }

    const ctxSignal = document.getElementById('signalChart').getContext('2d');
    const signalChart = new Chart(ctxSignal, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: '信号データ',
                data: data,
                borderColor: 'blue',
                borderWidth: 2,
                pointRadius: 0,
                stepped: true,
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: '時間 (μs)',
                    },
                },
                y: {
                    min: -0.1,
                    max: 1.1,
                    ticks: {
                        display: false
                    },
                    grid: {
                        drawTicks: false,
                        drawBorder: false
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            },
            maintainAspectRatio: false
        }
    });

    // ヒストグラムデータ作成
    const histogramPartial = createHistogramData(signalData, binWidth, false);
    const histogramFixed = createHistogramData(signalData, binWidth, true);

    const partialLabels = Object.keys(histogramPartial).map(Number);
    const partialPositiveCounts = Object.keys(histogramPartial).map(key => histogramPartial[key].positive);
    const partialNegativeCounts = Object.keys(histogramPartial).map(key => histogramPartial[key].negative);

    const fixedLabels = Object.keys(histogramFixed).map(Number);
    const fixedPositiveCounts = fixedLabels.map(label => histogramFixed[label].positive);
    const fixedNegativeCounts = fixedLabels.map(label => histogramFixed[label].negative);

    // ヒストグラムの描画
    drawHistogram(
        document.getElementById('histogramPartial').getContext('2d'),
        partialLabels,
        partialPositiveCounts,
        partialNegativeCounts
    );

    drawHistogram(
        document.getElementById('histogramFixed').getContext('2d'),
        fixedLabels,
        fixedPositiveCounts,
        fixedNegativeCounts
    );

    drawHistogram(
        document.getElementById('histogramSqrt').getContext('2d'),
        fixedLabels,
        fixedPositiveCounts.map(value => Math.sqrt(value)),
        fixedNegativeCounts,
        'sqrt'
    );
});
