var mysql = require('mysql');

require('dotenv').config()

var config = {
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME,
  connectionLimit: 10
};

var pool = mysql.createPool(config);

var getConnection = function(callback) {
  pool.getConnection(function(err, connection) {
    callback(err, connection);
  });
};

module.exports = getConnection;
