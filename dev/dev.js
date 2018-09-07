import { getTrials } from "./experiment.js";

$(document).ready(function() {
  $("form").submit(function() {
      let workerId = $("#workerId").val().slice();
      let setnum = Number($("#setnum").val().slice()) || 'NA';
      let assignmentId = undefined;
      let hitId = undefined;
      $("form").remove();
      getTrials(workerId, assignmentId, hitId, setnum);
  });
});
