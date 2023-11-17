import { ScatterEChart, EChartsOption } from "./EchartsBaseComponent/ScatterEChart";
import { Paper } from "@mui/material";

export interface CorrelationBetweenHindexAndExcludedArticlesType {
    correlation: number;
    data: DataType[];
}

interface DataType {
    'h-index': number;
    'document-count': number;
}

interface Props {
    data: CorrelationBetweenHindexAndExcludedArticlesType | undefined
}

export default function CorrelationBetweenHindexAndExcludedArticlesChart({data}: Props) {
    const scatterData = data?.data.map(item => [item['h-index'], item['document-count']]);
    const title = `H-index by Excluded Document Count, correlation: ${data?.correlation}`
    
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
                return 'H-index: ' + params.value[0] + '<br/>Document Count: ' + params.value[1];
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
            symbolSize: 5,
            data: scatterData,
        }]
    };

    return (
        <Paper sx={{ padding: 2}}>
            <ScatterEChart option={option} style={{height: '40rem'}}/>
        </Paper>
    )
}