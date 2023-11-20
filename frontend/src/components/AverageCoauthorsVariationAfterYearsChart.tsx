import { BarEChart, EChartsOption } from "./EchartsBaseComponent/BarEChart";
import { Paper } from "@mui/material";

export interface AverageCoauthorsVariationAfterYearsType {
    correlation: number;
    data: AvgCoauthorsCareerType[];
}

interface AvgCoauthorsCareerType {
    years_since_career_start: string;
    coauthors_count: number;
}

interface Props {
    data: AverageCoauthorsVariationAfterYearsType | undefined
}

export default function AverageCoauthorsVariationAfterYearsChart({data}: Props) {
    const years = data?.data.map(item => item.years_since_career_start);
    const coauthors = data?.data.map(item => item.coauthors_count);
    const title = `Average Coauthors over Career Years`
    const subtitle = `Corr.: ${Math.round(data?.correlation! * 10000) / 10000}`
    
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
            trigger: 'axis'
        },
        xAxis: {
            type: 'category',
            data: years,
            name: 'Years since career start',
            nameLocation: 'middle',
            nameGap: 25,
        },
        yAxis: {
            type: 'value',
            name: 'Coauthors count',
            nameLocation: 'middle',
            nameGap: 25,
            nameRotate: 90
        },
        series: [{
            name: title,
            data: coauthors,
            type: 'bar',
        }]
    };

    return (
        <Paper sx={{ padding: 2}}>
            <BarEChart option={option} style={{height: '20rem'}}/>
        </Paper>
    )
}