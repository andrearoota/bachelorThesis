import { BarEChart, EChartsOption } from "./EchartsBaseComponent/BarEChart";
import { Paper } from "@mui/material";

export interface CitationCountBasedOnConferenceRankingType {
    correlation: number;
    data: AvgByRatingType[]
  }

interface AvgByRatingType {
    GGS_Rating: string;
    citedby_count: number;
}

interface Props {
    data: CitationCountBasedOnConferenceRankingType | undefined
}

export default function CitationCountBasedOnConferenceRankingChart({data}: Props) {

    const filteredData: AvgByRatingType[] = data?.data.filter(item => !item.GGS_Rating.toLowerCase().includes('not')) ?? []

    const ratings = filteredData.map(item => item.GGS_Rating);
    const citedCounts = filteredData.map(item => item.citedby_count);
    const title = `Average Cited Count by GGS Rating, correlation: ${data?.correlation}`

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
            data: ratings,
            name: 'GGS Rating',
        },
        yAxis: {
            type: 'value',
            name: 'Cited by count'
        },
        series: [{
            name: title,
            data: citedCounts,
            type: 'bar',
        }]
    };

    return (
        <Paper sx={{ padding: 2}}>
            <BarEChart option={option} style={{height: '20rem'}}/>
        </Paper>
    )
}