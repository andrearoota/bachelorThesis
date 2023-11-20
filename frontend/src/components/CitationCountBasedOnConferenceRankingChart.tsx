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

    const item_order = ['C', 'B-', 'B', 'A-', 'A', 'A+', 'A++'];
    filteredData.sort((a, b) => item_order.indexOf(a.GGS_Rating) - item_order.indexOf(b.GGS_Rating));

    const ratings = filteredData.map(item => item.GGS_Rating);
    const citedCounts = filteredData.map(item => item.citedby_count);
    const title = `Average Citations per GGS Rating`
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
            data: ratings,
            name: 'GGS Rating',
            nameLocation: 'middle',
            nameGap: 25,
        },
        yAxis: {
            type: 'value',
            name: 'Cited by count',
            nameLocation: 'middle',
            nameGap: 25,
            nameRotate: 90
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