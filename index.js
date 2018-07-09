const express = require('express');
const bodyParser = require('body-parser');
const logger = require('morgan');
const professorRouter = require('./routes/ProfessorRouter.js');
const path = require('path');

const app = express();

// Serve static files from the React app
app.use(express.static(path.join(__dirname, 'client/build')));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(logger('dev'));

// Add routes
app.use('/api/professor', professorRouter);

// Error handler
app.use(function(err, req, res, next) {
  console.log(err.message);
  console.log("HI")
  res.status(err.status || 500).send(err.message);
});

// The "catchall" handler: for any request that doesn't
// match one above, send back React's index.html file.
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname+'/client/build/index.html'));
});

const port = process.env.PORT || 5000;
app.listen(port);

console.log(`Polyratings listening on ${port}`);
