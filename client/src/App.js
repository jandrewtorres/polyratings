import React, { Component } from 'react';
import './App.css';
import CssBaseline from '@material-ui/core/CssBaseline';
import Navbar from './Navbar';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import green from '@material-ui/core/colors/green';
import yellow from '@material-ui/core/colors/yellow';
import red from '@material-ui/core/colors/red';
import ProfessorTable from './ProfessorTable'

const theme = createMuiTheme({
  palette: {
    primary: green,
    secondary: yellow,
    error: red,
    // Used by `getContrastText()` to maximize the contrast between the background and
    // the text.
    contrastThreshold: 3,
    // Used to shift a color's luminance by approximately
    // two indexes within its tonal palette.
    // E.g., shift from Red 500 to Red 300 or Red 700.
    tonalOffset: 0.2,
  },
});


class App extends Component {
  // Initialize state
  state = { professors: [] }

  // Fetch professors after first mount
  componentDidMount() {
    this.getProfessors();
  }

  getProfessors = () => {
    // Get the professors and store them in state
    fetch('/api/professor')
      .then(res => res.json())
      .then(professors => this.setState({ professors }));
  }

  render() {
    const { professors } = this.state;

    return (
      <MuiThemeProvider theme={theme}>
        <React.Fragment>
          <CssBaseline />
          <Navbar />
          <ProfessorTable data = { professors }/>
        </React.Fragment>
      </MuiThemeProvider>
    );
  }
}

export default App;
