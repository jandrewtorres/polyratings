import React from 'react';
// import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

const styles = theme => ({
  root: {
    width: '100%',
    overflowX: 'auto',
  },
  table: {
    minWidth: 700,
  },
});


function ProfessorTable(props) {
  const { classes, data } = props;

  return (
    <Paper className={classes.root}>
      <Table className={classes.table}>
        <TableHead>
          <TableRow>
            <TableCell>Last Name</TableCell>
            <TableCell>First name</TableCell>
            <TableCell>Department</TableCell>
            <TableCell>Overall Rating</TableCell>
            <TableCell>Difficulty Rating</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map(n => {
            return (
              <TableRow key={n.id}>
                <TableCell component="th" scope="row">
                  {n.first_name}
                </TableCell>
                <TableCell>{n.last_name}</TableCell>
                <TableCell>{n.department}</TableCell>
                <TableCell>{n.rating_overall}</TableCell>
                <TableCell>{n.rating_difficulty}</TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </Paper>
  );
}
/*
SimpleTable.propTypes = {
  classes: PropTypes.object.isRequired,
};
*/

export default withStyles(styles)(ProfessorTable);
