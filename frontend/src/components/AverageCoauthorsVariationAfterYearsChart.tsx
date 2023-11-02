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
    const title = `Average Coauthors over Career Years, correlation: ${data?.correlation}`
    
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
            trigger: 'axis'
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: years,
            name: 'Years since\n career start',
        },
        yAxis: {
            type: 'value',
            name: 'Coauthors count'
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