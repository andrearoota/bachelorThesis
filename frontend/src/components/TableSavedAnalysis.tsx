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
import { Box, Button, Typography } from '@mui/material';

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

  return (
    <Paper sx={{ width: '100%' }}>
      <Typography variant="h6" padding={2} paddingBottom={0}>
        View old analysis
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
                        <Button variant="contained" endIcon={<VisibilityIcon />} size="small" onClick={() => {setAnalysisShow(row)}}>
                          View
                        </Button>
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