import { HeatmapEChart, EChartsOption } from "./EchartsBaseComponent/HeatmapEChart";
import { Paper } from "@mui/material";

export interface AnalyzeHindexInfluentialArticlesTimingType {
    weight_career_avg: number;
    data: number[];
}

interface Props {
    data: AnalyzeHindexInfluentialArticlesTimingType | undefined
}

type OccurencesType = Record<number, number>;


export default function AnalyzeHindexInfluentialArticlesTimingChart({data}: Props) {
    const occurrences: OccurencesType = {};

    data?.data.forEach(value => {
        const rounded = Math.round(value * 100) / 100; // Arrotondiamo alla seconda cifra decimale
        occurrences[rounded] = (occurrences[rounded] || 0) + 1;
    });
    
    // Convertiamo l'oggetto in un array per ECharts
    const heatmapData = [];
    for (const key in occurrences) {
        heatmapData.push([parseFloat(key), 0, occurrences[key]]);
    }
    heatmapData.sort((a, b) => a[0] - b[0]);

    const title = `Heatmap of Weight Career`
    const subtitle = `AVG: ${Math.round(data?.weight_career_avg! * 10000) / 10000}`

    const option: EChartsOption = {
        title: {
            text: title,
            subtext: subtitle,
            left: 'center'
        },
        toolbox: {
            feature: {
              saveAsImage: {},
              dataView: {
                readOnly: true
              },
            }
        },
        tooltip: {
            position: 'right',
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            formatter: function(params: any) {
                return 'Value: ' + params.data[0] + '<br>Count: ' + params.data[2];
            }
        },
        yAxis: {
            type: 'category',
            data: ['Count'],
            nameLocation: 'middle',
            nameGap: 25,
        },
        xAxis: {
            type: 'category',
            name: 'Value',
            nameLocation: 'middle',
            nameGap: 25,
        },
        visualMap: {
            min: 1,
            max: Math.max(...Object.values(occurrences)),
            calculable: true,
            orient: 'horizontal',
            left: 'center',
        },
        series: [{
            name: 'Weight Career',
            type: 'heatmap',
            data: heatmapData,
            label: {
                show: false
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              },
        }]
    };

    return (
        <Paper sx={{ padding: 2}}>
            <HeatmapEChart option={option} style={{height: '40rem'}}/>
        </Paper>
    )
}