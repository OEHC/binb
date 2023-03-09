'use strict';

const redis = require('redis');

/**
 * Allow for two separatation between user and track database.
 * If not specified, bot attempt to connect to localhost at port 6379.
 * The track database url/port can be set with the environment variables
 * REDIS_URL and REDIS_PORT, and the user database url/port with REDIS_USER_URL
 * and REDIS_USER_PORT. If REDIS_USER_* is no specified, REDIS_* env variables
 * will be used before the default values.
 */

const db   = process.env.REDIS_URL || 'localhost';
const port = process.env.REDIS_PORT || 6379;

const user_db   = process.env.REDIS_USER_URL || process.env.REDIS_URL || 'localhost';
const user_port = process.env.REDIS_USER_PORT || process.env.REDIS_PORT || 6379;

/**
 * Setting up redis clients.
 */

const songsclient = redis.createClient({ host: db, port: port, auth_pass: process.env.DB_AUTH });
const usersclient = redis.createClient({ host: user_db, port: user_port, auth_pass: process.env.DB_AUTH });

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
