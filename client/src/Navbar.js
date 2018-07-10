import React, {Component} from 'react'
// import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import InputAdornment from '@material-ui/core/InputAdornment';
import Search from '@material-ui/icons/Search';

const styles = theme => ({
  root: {
    marginTop: theme.spacing.unit *3,
    width: '100%',
  },
  flex: {
    flex: 2,
  },
  search: {
    flex: 1,
    marginLeft: theme.spacing.unit * 3,
    backgroundColor: theme.palette.primary.light,
    borderRadius: 5,
  },
  appbar: {
    backgroundColor: theme.palette.primary.dark,
    color: theme.palette.common.white
  }
})

class Navbar extends Component {
  render() {
    const {classes} = this.props;

    return (
      <AppBar color="inherit" position="static" elevation={0} className={classes.appbar}>
        <Toolbar>
          <Typography variant="title" color="inherit" className={classes.flex}>
            PolyRatings
          </Typography>
          <Button color="inherit">Browse</Button>
          <Button color="inherit">Post Review</Button>
          <TextField
            color="inherit"
            className={classes.search}
            InputProps={{
              disableUnderline: true,
              startAdornment: (
                <InputAdornment position="start">
                  <Search />
                </InputAdornment>
              ),
            }}
          />
        </Toolbar>
      </AppBar>
    )
  }
}
/*
Navbar.propTypes = {
  classes: PropTypes.object.isRequired
};
*/
export default withStyles(styles)(Navbar);
