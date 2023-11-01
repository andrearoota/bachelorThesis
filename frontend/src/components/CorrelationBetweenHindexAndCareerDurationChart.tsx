import { ScatterEChart, EChartsOption } from "./EchartsBaseComponent/ScatterEChart";
import { Paper } from "@mui/material";

export interface CorrelationBetweenHindexAndCareerDurationType {
    correlation: number;
    data: DataType[];
}

interface DataType {
    'h-index': number;
    duration_career: number;
}

interface Props {
    data: CorrelationBetweenHindexAndCareerDurationType | undefined
}

export default function CorrelationBetweenHindexAndCareerDurationChart({data}: Props) {
    const scatterData = data?.data.map(item => [item['h-index'], item.duration_career]);
    const title = `H-index by Duration career, correlation: ${data?.correlation}`
    
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
                return 'H-index: ' + params.value[0] + '<br/>Duration career: ' + params.value[1];
            }
        },
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