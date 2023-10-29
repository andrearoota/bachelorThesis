import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Unstable_Grid2';
import { Typography } from '@mui/material';
import React from 'react';
import TableSavedAnalysis from './components/TableSavedAnalysis';
import FormNewAnalysis from './components/FormNewAnalysis';
import AverageCoauthorsVariationAfterYearsChart, { AverageCoauthorsVariationAfterYearsType } from './components/AverageCoauthorsVariationAfterYearsChart';
import CitationCountBasedOnConferenceRankingChart, { CitationCountBasedOnConferenceRankingType } from './components/CitationCountBasedOnConferenceRankingChart';
import AnalyzeHindexInfluentialArticlesTimingChart, { AnalyzeHindexInfluentialArticlesTimingType } from './components/analyzeHindexInfluentialArticlesTimingChart';
import CoauthorsImpactOnCitationsAndHindexChart, { CoauthorsImpactOnCitationsAndHindexType } from './components/CoauthorsImpactOnCitationsAndHindexChart';
import CorrelationBetweenHindexAndCareerDurationChart, { CorrelationBetweenHindexAndCareerDurationType } from './components/CorrelationBetweenHindexAndCareerDurationChart';
import CorrelationBetweenHindexAndExcludedArticlesChart, { CorrelationBetweenHindexAndExcludedArticlesType } from './components/CorrelationBetweenHindexAndExcludedArticlesChart';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

export interface Analysis {
  _id: {
    $oid: string;
  };
  name: string;
  'h-index': number;
  datetime: {
    $date: string;
  };
  data: {
    [key: string]: unknown;
  };
}

export default function App() {
  const [savedAnalysys, setSavedAnalyses] = React.useState<Analysis[]>([])
  const [analysisShow, setAnalysisShow] = React.useState<Analysis>()

  React.useEffect(() => {
    fetch('http://localhost/api/saved_analyses')
    .then(response => response.json())
    .then(data => {
      setSavedAnalyses(data)
    })
    .catch(error => {
      alert(error)
    });
  }, [])

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        <Grid xs={12}>
            <Grid container spacing={2}>
              <Grid xs>
                <TableSavedAnalysis setAnalysisShow={setAnalysisShow} rows={savedAnalysys} />
              </Grid>
              <Grid xs={1} display='flex' flexDirection='column' justifyContent='center'>
                <Typography variant="h6" gutterBottom>
                  or
                </Typography>
              </Grid>
              <Grid xs display='flex' flexDirection='column' justifyContent='center' spacing={2}>
                <FormNewAnalysis setAnalysisShow={setAnalysisShow} setSavedAnalyses={setSavedAnalyses}></FormNewAnalysis>
              </Grid>
            </Grid>            
        </Grid>
        <Grid xs={12}>
          <Typography variant="h6" gutterBottom>
            Output
          </Typography>
        </Grid>
        <Grid xs={12}>
          <AverageCoauthorsVariationAfterYearsChart data={analysisShow?.data.average_coauthors_variation_after_years as AverageCoauthorsVariationAfterYearsType} />
        </Grid>
        <Grid xs={12}>
          <CitationCountBasedOnConferenceRankingChart data={analysisShow?.data.citation_count_based_on_conference_ranking as CitationCountBasedOnConferenceRankingType} />
        </Grid>
        <Grid xs={6}>
          <CoauthorsImpactOnCitationsAndHindexChart data={analysisShow?.data.coauthors_impact_on_citations_and_hindex as CoauthorsImpactOnCitationsAndHindexType} />
        </Grid>
        <Grid xs={6}>
          <AnalyzeHindexInfluentialArticlesTimingChart data={analysisShow?.data.analyze_hindex_influential_articles_timing as AnalyzeHindexInfluentialArticlesTimingType} />
        </Grid>
        <Grid xs={6}>
          <CorrelationBetweenHindexAndCareerDurationChart data={analysisShow?.data.correlation_between_hindex_and_career_duration as CorrelationBetweenHindexAndCareerDurationType} />
        </Grid>
        <Grid xs={6}>
          <CorrelationBetweenHindexAndExcludedArticlesChart data={analysisShow?.data.correlation_between_hindex_and_excluded_articles as CorrelationBetweenHindexAndExcludedArticlesType} />
        </Grid>
      </Grid>
    </Box>
  );
}