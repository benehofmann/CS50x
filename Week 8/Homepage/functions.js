function sendMessage() {
  if (ValidateEmail() === true) {
    var reason = document.getElementsByName("optradio")
    // 1st case "Sign Membership"
    if (document.getElementById("Membership").checked) {
      alert("Submit successfull! You will soon get your Contract to sign your Membership")

    } else {
      for (var i = 0; i < reason.length; i++) {
        if (reason[i].checked) {
          alert("Your contact reason: " + document.getElementById("txtBox").value + "\nYou will soon get a Message from us!")
        }
      }
    }
  } else
    alert("error")



}


function ValidateEmail() {
  if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(document.querySelector("#email").value)) {
    return (true)
  }
  alert("You have entered an invalid email address!")
  return (false)
}

function ShowHideDiv() {
  var chkOther = document.getElementById("other");
  var chkFeedback = document.getElementById("Feedback")
  var dvtext = document.getElementById("dvtext");
  if (chkOther.checked == true || chkFeedback.checked == true) {
    dvtext.style.display = "block"
  } else
    dvtext.style.display = "none"


}



