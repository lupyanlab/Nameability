import demographicsQuestions from "./demographics.js";

const PORT = 7072;
const FULLSCREEN = false;

export function getTrials(workerId='NA', assignmentId='NA', hitId='NA') {
  
  $("#loading").html('Loading trials... please wait. </br> <img src="img/preloader.gif">')
  
  // This calls server to run python generate trials (judements.py) script
  // Then passes the generated trials to the experiment
  $.ajax({
      url: 'http://'+document.domain+':'+PORT+'/trials',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({workerId: workerId}),
      success: function (data) {
          console.log(data);
          $("#loading").remove();
  
          runExperiment(data.trials, workerId, assignmentId, hitId, PORT, FULLSCREEN);
      }
  })
}

function disableScrollOnSpacebarPress () {
  window.onkeydown = function(e) {
    if (e.keyCode == 32 && e.target == document.body) {
      e.preventDefault();
    }
  };
}

// Function Call to Run the experiment
function runExperiment(trials, workerId, assignmentId, hitId, PORT, FULLSCREEN) {
  disableScrollOnSpacebarPress();

  let timeline = [];

  // Data that is collected for jsPsych
  let turkInfo = jsPsych.turk.turkInfo();
  let participantID = makeid() + "iTi" + makeid();

  jsPsych.data.addProperties({
    subject: participantID,
    condition: "explicit",
    group: "shuffled",
    assginementId: assignmentId,
    hitId: hitId
  });

  // sample function that might be used to check if a subject has given
  // consent to participate.
  var check_consent = function (elem) {
    if ($('#consent_checkbox').is(':checked')) {
        return true;
    }
    else {
        alert("If you wish to participate, you must check the box next to the statement 'I agree to participate in this study.'");
        return false;
    }
    return false;
  };
  // declare the block.
  var consent = {
    type: 'external-html',
    url: "./consent.html",
    cont_btn: "start",
    check_fn: check_consent
  };

  timeline.push(consent);

  let continue_space =
    "<div class='right small'>Press SPACE to continue.</div>";

  let instructions = {
    type: "instructions",
    key_forward: 'space',
    key_backward: 'backspace',
    pages: [
      `<p>On each page you will see two pictures from the same category e.g., two cats. Your task is simply to decide which of the two pictures is the best example of your idea or image of what the category is. The categories you will see are <b>cats, dogs, birds, fish, cars, trains, planes and boats</b>.
      <p><b>Use the keys 1-5 to respond</b>. You will be asked to about 225 judgments. Estimated total time is 5-6 minutes. At the end, you will get a completion code.
            </p> ${continue_space}`
    ]
  };

  timeline.push(instructions);

  // keeps track of current trial progression
  // and used for the progress bar
  let progress_number = 1;
  let images = [];
  let num_trials = trials.length;

  trials.forEach((trial, index) => {
    // In contrast to progress_number,
    // trial_number is used for recording
    // responses
    const trial_number = index + 1;

    images.push("images/" + trial.Image);

    // Empty Response Data to be sent to be collected
    let response = {
      workerId: workerId,
      assignmentId: assignmentId,
      hitId: hitId,
      set: trial.set,
      ProblemType: trial.ProblemType,
      PartID: trial.PartID,
      Image: trial.Image,
      file: trial.file,
      expTimer: -1,
      response: -1,
      trial_number: trial_number,
      rt: -1
    };
    
    const image = trial.Image;
    
    let stimulus = /*html*/`
        <h5 style="text-align:center;margin-bottom:20%;margin-top:0;">Trial ${trial_number} of ${num_trials}</h5>
        <div style="width:100%;">
          <img src="images/${image}" alt="${image}"/>   
        </div>
    `;
    
    // Picture Trial
    let jsPsychTrial = {
      type: "text-area",

      stimulus: stimulus,
      question: "Please describe the highlighted image",
      placeholder: "Your answer here...",
      trim_response_string: true,

      on_finish: function(data) {
        // response.response = String.fromCharCode(data.key_press);
        // response.choice = choices[Number(response.response)-1];
        response.response = data.response;
        response.rt = data.rt;
        response.expTimer = data.time_elapsed / 1000;

        // POST response data to server
        $.ajax({
          url: "http://" + document.domain + ":" + PORT + "/data",
          type: "POST",
          contentType: "application/json",
          data: JSON.stringify(response),
          success: function() {
            console.log(response);
            jsPsych.setProgressBar((progress_number - 1) / num_trials);
            progress_number++;
          }
        });
      }
    };
    timeline.push(jsPsychTrial);
  });


  let questionsInstructions = {
    type: "instructions",
    key_forward: 'space',
    key_backward: 'backspace',
    pages: [
        `<p class="lead">We'll now ask you a few demographic questions and we'll be done!
          </p> ${continue_space}`,
    ]
  };

  timeline.push(questionsInstructions);

  let demographicsTrial = {
      type: 'surveyjs',
      questions: demographicsQuestions,
      on_finish: function (data) {
          let demographicsResponses = data.response;
          console.log(demographicsResponses);
          let demographics = Object.assign({ workerId }, demographicsResponses);
          // POST demographics data to server
          $.ajax({
              url: 'http://' + document.domain + ':' + PORT + '/demographics',
              type: 'POST',
              contentType: 'application/json',
              data: JSON.stringify(demographics),
              success: function () {
              }
          })

  let endmessage = `Thank you for participating! Your completion code is ${participantID}. Copy and paste this in 
        MTurk to get paid. 

        <p>The purpose of this HIT is to assess the extent to which different people agree what makes
        a particular dog, cat, or car typical.
        
        <p>
        If you have any questions or comments, please email hroebuck@wisc.edu.`;
          jsPsych.endExperiment(endmessage);
      }
  };
  timeline.push(demographicsTrial);

  let endmessage = `Thank you for participating! Your completion code is ${participantID}. Copy and paste this in 
        MTurk to get paid. 

        <p>The purpose of this HIT is to assess the extent to which different people agree what makes
        a particular dog, cat, or car typical.
        
        <p>
        If you have any questions or comments, please email hroebuck@wisc.edu.`;

    
  Promise.all(images.map((image, index) => {
    return loadImage(image)
    .catch((error) => {
      console.warn("Removing trial with image, " + image);
      trials[index] = null;
    });
  }))
  .then((images) => {
    trials = trials.filter((trial, index) => {
      return trial !== null;
    });
    startExperiment();
  })

  function startExperiment() {
    jsPsych.init({
      timeline: timeline,
      fullscreen: FULLSCREEN,
      show_progress_bar: true,
      auto_update_progress_bar: false
    });
  }
}
