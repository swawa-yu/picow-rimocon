function parseSignalData(signalData, T) {
    const dataBits = [];
    for (let i = 2; i < signalData.length - 2; i += 2) {
        const evenDuration = signalData[i];
        const oddDuration = Math.abs(signalData[i + 1]);

        if (Math.abs(evenDuration - T) > T * 0.5) {
            throw new Error("データの構造が適合しません (Tに誤りがあります)");
        }

        const bit = oddDuration > T * 2 ? 0 : 1;
        dataBits.push(bit);
    }
    return dataBits;
}

function createHistogramData(signalData, binWidth, isFixedScale = true) {
    const bins = {};
    const maxValue = isFixedScale
        ? Math.max(...signalData.map(Math.abs))
        : Math.max(...signalData);

    const binCount = Math.ceil(maxValue / binWidth);

    for (let i = 0; i <= binCount; i++) {
        bins[i * binWidth] = { positive: 0, negative: 0 };
    }

    signalData.forEach(value => {
        const absValue = Math.abs(value);
        const bin = Math.floor(absValue / binWidth) * binWidth;
        if (value > 0) {
            bins[bin].positive++;
        } else {
            bins[bin].negative++;
        }
    });

    return bins;
}
