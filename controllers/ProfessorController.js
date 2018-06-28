const db = require('../dbconnection');

// Get all professors data
exports.professorsList = function(req, res, next) {
  const sql = "select * from professor";
  db(function(err, conn) {
    if (err) next(err);
    conn.query(sql, function(err, results) {
      conn.release();
      if(err) next(err);
      res.json(results);
    });
  });
};

// Get single professor data
exports.professorDetail = function(req, res, next) {
  const sql = "select * from professor as p where p.pid = ?";
  db(function(err, conn) {
    if(err) next(err);
    conn.query(sql, [req.params.id], function(err, results) {
      conn.release();
      if(err) next(err);
      res.json(results);
    });
  });
};

// Insert new professor
exports.professorCreate = function(req, res, next) {
  res.send('NOT IMPLEMENTED: Professor create')
};

// Delete professor
exports.professorDelete = function(req, res, next) {
  res.send('NOT IMPLEMENTED: Professor delete')
};

// Update professor
exports.professorUpdate = function(req, res, next) {
  res.send('NOT IMPLEMENTED: Professor update')
};
