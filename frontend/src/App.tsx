import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Unstable_Grid2';
import { Typography } from '@mui/material';
import React from 'react';
import TableSavedAnalysis from './components/TableSavedAnalysis';
import FormNewAnalysis from './components/FormNewAnalysis';
import CorrCoauthorsCareerChart, { CorrCoauthorsCareerType } from './components/CorrCoauthorsCareerChart';
import CorrRatingCitedByChart, { CorrRatingCitedType } from './components/CorrRatingCitedByChart';

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
  const [savedAnalysys, setSavedAnalysis] = React.useState<Analysis[]>([])
  const [analysisShow, setAnalysisShow] = React.useState<Analysis>()

  React.useEffect(() => {
    fetch('http://localhost/api/saved-analysis')
    .then(response => response.json())
    .then(data => {
      setSavedAnalysis(data)
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
                <FormNewAnalysis setAnalysisShow={setAnalysisShow} setSavedAnalysis={setSavedAnalysis}></FormNewAnalysis>
              </Grid>
            </Grid>            
        </Grid>
        <Grid xs={12}>
          <Typography variant="h6" gutterBottom>
            Output
          </Typography>
        </Grid>
        <Grid xs={12}>
          <CorrCoauthorsCareerChart data={analysisShow?.data.corr_coauthors_career as CorrCoauthorsCareerType} />
        </Grid>
        <Grid xs={12}>
          <CorrRatingCitedByChart data={analysisShow?.data.corr_rating_citedby as CorrRatingCitedType} />
        </Grid>
      </Grid>
    </Box>
  );
}