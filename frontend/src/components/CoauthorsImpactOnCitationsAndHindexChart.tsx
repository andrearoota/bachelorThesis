import { ScatterEChart, EChartsOption } from "./EchartsBaseComponent/ScatterEChart";
import { Paper } from "@mui/material";

export interface CoauthorsImpactOnCitationsAndHindexType {
    correlation: number;
    data: DataType[];
}

interface DataType {
    author_count: number;
    citedby_count: number;
}

interface Props {
    data: CoauthorsImpactOnCitationsAndHindexType | undefined
}

export default function CoauthorsImpactOnCitationsAndHindexChart({data}: Props) {
    const scatterData = data?.data.map(item => [item.author_count, item.citedby_count]);
    const title = `Citations by Author Count, correlation: ${data?.correlation}`
    
    const option: EChartsOption = {
        title: {
            text: title
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
            trigger: 'item',
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            formatter: function(params: any) {
                return 'Author count: ' + params.value[0] + '<br/>Cited by count: ' + params.value[1];
            }
        },
        /* grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        }, */
        xAxis: {
            type: 'value',
            name: 'Author count',
            min: 'dataMin',
            max: 'dataMax'
        },
        yAxis: {
            type: 'value',
            name: 'Cited by count',
            min: 'dataMin',
            max: 'dataMax'
        },
        dataZoom: [
            {
              type: 'slider',
              yAxisIndex: 0
            },
            {
                type: 'slider',
                xAxisIndex: 0
            },
        ],
        series: [{
            type: 'scatter',
            data: scatterData,
        }]
    };

    return (
        <Paper sx={{ padding: 2}}>
            <ScatterEChart option={option} style={{height: '40rem'}}/>
        </Paper>
    )
}