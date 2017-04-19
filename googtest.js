/**
 * Copyright 2016, Google, Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// [START vision_quickstart]
// Imports the Google Cloud client library
var google = require('@google-cloud');

var vision = require('@google-cloud/vision')({
  projectId: 'vision-play-165021',
  keyFilename: '/home/pi/keys/vision-play-40d1a084e616.json'
});

google.auth.getApplicationDefault(function(err, authClient) {
   if (err) {
     return cb(err);
   }});


// The name of the image file to annotate
var fileName = './photos/test_truck.jpg';

// Performs label detection on the image file
vision.detectLabels(fileName)
  .then(function (results) {
    var labels = results[0];

    console.log('Labels:');
    console.log(labels);
  })
  .catch(function (err) {
    console.error('ERROR:', err);
  });
// [END vision_quickstart]