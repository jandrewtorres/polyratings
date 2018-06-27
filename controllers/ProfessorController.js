const db = require('../dbconnection');

// Get all professors data
exports.professorsList = function(req, res) {
  db(function(err, conn) {
    if (err) throw err;
    conn.query("select * from professor", function(err, rows) {
      if(err) throw err;
      res.json(rows);
    });
    conn.release();
  });
};

// Get single professor data
exports.professorDetail = function(req, res) {
  res.send('NOT IMPLEMENTED: Professor detail')
};

// Insert new professor
exports.professorCreate = function(req, res) {
  res.send('NOT IMPLEMENTED: Professor create')
};

// Delete professor
exports.professorDelete = function(req, res) {
  res.send('NOT IMPLEMENTED: Professor delete')
};

// Update professor
exports.professorUpdate = function(req, res) {
  res.send('NOT IMPLEMENTED: Professor update')
};
