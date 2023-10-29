import { BarEChart, EChartsOption } from "./EchartsBaseComponent/BarEChart";
import { Paper } from "@mui/material";

export interface CorrRatingCitedType {
    correlation: number;
    avg_by_rating: AvgByRatingType[]
  }

interface AvgByRatingType {
    GGS_Rating: string;
    citedby_count: number;
}

interface Props {
    data: CorrRatingCitedType | undefined
}

export default function CorrRatingCitedByChart({data}: Props) {

    const ratings = data?.avg_by_rating.map(item => item.GGS_Rating);
    const citedCounts = data?.avg_by_rating.map(item => item.citedby_count);
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