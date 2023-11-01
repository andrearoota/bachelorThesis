import * as React from 'react';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import VisibilityIcon from '@mui/icons-material/Visibility';
import { Analysis } from '../App';
import { Box, Button, Stack, Typography } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import { getInstanceByDom, ECharts } from 'echarts/core'
import JSZip from 'jszip';
import { saveAs } from 'file-saver';

interface Props {
  rows: Analysis[];
  setAnalysisShow: React.Dispatch<React.SetStateAction<Analysis | undefined>>;
}

export default function TableSavedAnalysis({rows, setAnalysisShow}: Props) {
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(5);

  const handleChangePage = (_event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  const setDataAndDownload = (data: Analysis) => {
    setAnalysisShow(data)
    setTimeout(exportData, 1000, data);
  };

  const exportData = (data: Analysis) => {
    const zip = new JSZip();
    const analysis = zip.folder('analysis');
    
    getAllInstances().forEach((instance: ECharts, index: number) => {
      const data = decodeURIComponent(instance.getDataURL());
      analysis?.file(`chart-${index}.svg`, data.substring(data.indexOf(',') + 1));
    });

    analysis?.file(`${data.name}.json`, JSON.stringify(data));

    zip.generateAsync({type:'blob'})
    .then(function(content) {
      saveAs(content, `${data.name}.zip`);
    });

  };

  const getAllInstances = (): ECharts[] => {
    const instances: ECharts[] = [];
    // Probably will break down in the future
    document.querySelectorAll('canvas[_echarts_instance_], div[_echarts_instance_]').forEach(
      function(e: Element) {
        const instance: ECharts | undefined = getInstanceByDom(e as HTMLElement);
        if(instance){
            instances.push(instance);
        }        
      }
    );
    return instances;
}


  return (
    <Paper sx={{ width: '100%' }}>
      <Typography variant="h6" padding={2} paddingBottom={0}>
        View old analyses
      </Typography>
      <Box padding={2}>
        <TableContainer sx={{ maxHeight: 440 }}>
        <Table stickyHeader aria-label="sticky table">
            <TableHead>
              <TableRow>
                  <TableCell
                    key={'name'}
                  >
                    name
                  </TableCell>
                  <TableCell
                    key={'h-index'}
                  >
                    h-index
                  </TableCell>
                  <TableCell
                    key={'datetime'}
                  >
                    datetime
                  </TableCell>
                  <TableCell
                    key={'action'}
                  >
                  </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((row) => {
                  const date = new Date(row.datetime.$date)
                  return (
                    <TableRow hover role="checkbox" tabIndex={-1} key={row._id.$oid}>
                      <TableCell>
                        {row.name}
                      </TableCell>
                      <TableCell>
                        {row['h-index']}
                      </TableCell>
                      <TableCell>
                        {date.toLocaleString()}
                      </TableCell>
                      <TableCell>
                        <Stack direction="row" spacing={2}>
                          <Button variant="contained" endIcon={<VisibilityIcon />} size="small" onClick={() => {setAnalysisShow(row)}}>
                            View
                          </Button>
                          <Button variant="contained" endIcon={<DownloadIcon />} size="small" onClick={() => {setDataAndDownload(row)}}>
                            Download
                          </Button>
                        </Stack>
                      </TableCell>
                    </TableRow>
                  );
                })}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 20]}
          component="div"
          count={rows.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Box>
      
    </Paper>
  );
}