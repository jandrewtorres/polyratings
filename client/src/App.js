import React, { Component } from 'react';
import './App.css';

class App extends Component {
  // Initialize state
  state = { professors: [] }

  // Fetch professors after first mount
  componentDidMount() {
    this.getProfessors();
  }

  getProfessors = () => {
    // Get the professors and store them in state
    fetch('/api/professors')
      .then(res => res.json())
      .then(professors => this.setState({ professors }));
  }

  render() {
    const { professors } = this.state;

    return (
      <div className="App">
        {/* Render the professors if we have them */}
        {professors.length ? (
          <div>
            <h1>All professors</h1>
            <ul className="professors">
              {/*
                Generally it's bad to use "index" as a key.
                It's ok for this example because there will always
                be the same number of professors, and they never
                change positions in the array.
              */}
              {professors.map((professor, index) =>
                <li key={index}>
                  {professor.f_name}
                </li>
              )}
            </ul>
          </div>
        ) : (
          // Render a helpful message otherwise
          <div>
            <h1>No professors :(</h1>
            <button
              className="more"
              onClick={this.getProfessors}>
              Try Again?
            </button>
          </div>
        )}
      </div>
    );
  }
}

export default App;
