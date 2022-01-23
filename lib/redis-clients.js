'use strict';

const redis = require('redis');
const db = process.env.REDIS_URL || 'localhost';
const port = process.env.REDIS_PORT || 6379;

/**
 * Setting up redis clients.
 */

const songsclient = redis.createClient({ host: db, port: port, auth_pass: process.env.DB_AUTH });
const usersclient = redis.createClient({ host: db, port: port, auth_pass: process.env.DB_AUTH });

songsclient.on('error', function(err) {
  console.error(err.message);
});

usersclient.on('error', function(err) {
  console.error(err.message);
});

usersclient.select(1);

/**
 * Expose the clients
 */

exports.songs = songsclient;
exports.users = usersclient;
