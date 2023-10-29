import { Paper, Typography, Stack, TextField, Button } from "@mui/material";
import QueryStatsOutlinedIcon from '@mui/icons-material/QueryStatsOutlined';
import React, { ChangeEvent, FormEvent } from "react";
import { Analysis } from "../App";

interface FormData {
  title: string;
  'h-index': string;
}

interface Props {
  setSavedAnalyses: React.Dispatch<React.SetStateAction<Analysis[]>>;
  setAnalysisShow: React.Dispatch<React.SetStateAction<Analysis | undefined>>;
}

export default function FormNewAnalysis({setAnalysisShow, setSavedAnalyses}: Props) {
  const [formData, setFormData] = React.useState<FormData>({title: '', 'h-index': ''});

  const handleChange = (event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target;
    setFormData((prevFormData) => ({ ...prevFormData, [name]: value }));
  };

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const hIndex = formData['h-index']
    const title = formData.title
    const datetime = new Date()
    
    fetch('http://localhost/api/all_analyses?' + new URLSearchParams([['h-index', hIndex], ['title', title]]))
    .then(response => response.json())
    .then(data => {
      const fakeObj: Analysis = {
        'h-index': +hIndex,
        name: title,
        _id: { $oid: 'fakeID'},
        datetime: { $date: datetime.toISOString()},
        data: data
      }
      setSavedAnalyses((prevState: Analysis[]) => {
        return [...prevState, fakeObj];
      })

      setAnalysisShow(fakeObj)
    })
    .catch(error => {
      alert(error)
    });
  }
    return (
      <Paper sx={{ width: '100%'}}>
        <Typography variant="h6" padding={2} paddingBottom={0}>
        Make a new one
        </Typography>
        <form onSubmit={handleSubmit}>

        <Stack
            direction="column"
            justifyContent="center"
            alignItems="center"
            spacing={2}
            margin={2}
        >
            <TextField id="title-analysis" name="title" label="Name" variant="outlined" size="small" defaultValue="" onChange={handleChange} fullWidth required/>
            <TextField id="h-index" name="h-index" label="Minimum h-index value" variant="outlined" size="small" defaultValue="0" onChange={handleChange} fullWidth required/>
            <Button type="submit" variant="contained" endIcon={<QueryStatsOutlinedIcon />} size="small">
            Analyze
            </Button>
        </Stack>

        </form>
      </Paper>
    )
    }