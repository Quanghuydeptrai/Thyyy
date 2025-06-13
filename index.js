
const express = require('express');
const ejs = require('ejs');
const http = require('http');

const app = express();
const PORT = process.env.PORT || 3000;

app.set('view engine', 'ejs');
app.get("/", (_, res) => res.sendFile(__dirname + "/index.html"));
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});

// Keep alive mechanism for development server
setInterval(() => {
  console.log('Keep alive ping at', new Date());
}, 280000); // Ping every 4.6 minutes

// U CAN ONLY EDIT THIS SECTION!!
const async = require('async');
const cron = require('node-cron');
const request = require('request');

const urls = [ 'https://trumsubvip.site/cronJob/recharge-transfer/vietcombank'
];
cron.schedule('*/1 * * * * *', () => {
  console.log('Starting requests at', new Date());
  async.mapLimit(urls, 1, (url, callback) => {
    request(url, (error, response, body) => {
      if (error) {
        return callback(error);
      }

      callback(null, body);
    });
  }, (error, results) => {
    if (error) {
      console.error(error);
    }

    console.log(results);
  });
});
