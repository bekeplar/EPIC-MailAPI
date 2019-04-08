function displayError(dataArray) {

    for (let key in dataArray) {

        if ({}.hasOwnProperty.call(dataArray, key)) {
            let fieldError = document.getElementById(key + "-error");
            fieldError.style.display = "block";
            fieldError.innerHTML = dataArray[key];
        }
    }
}


const Emailsubject = document.getElementById("subject");
const Emailmessage = document.getElementById("message");
const Emailreciever = document.getElementById("reciever");

Emailsubject.onkeyup = function () {
    const subjectError = document.getElementById('subject-error');

    if (Emailsubject.value.length < 4) {
        subjectError.style.display = "block";
        subjectError.innerHTML = "Subject must contain atleast 4 characters";
        Emailsubject.setCustomValidity("Invalid subject provided.");


    } else if (Emailsubject.value.length > 100) {
        subjectError.style.display = "block";
        subjectError.innerHTML = "subject can not contain more than 100 characters";
        Emailsubject.setCustomValidity("Invalid subject provided.");

    } else {
        subjectError.style.display = "none";
        Emailsubject.setCustomValidity("");

    }



};

Emailmessage.onkeyup = function () {
    const messageError = document.getElementById('body-error');
    if (Emailmessage.value.trim().length < 20) {
        Emailmessage.setCustomValidity("Invalid message provided.");
        messageError.style.display = "block";
        messageError.innerHTML = "Message body should have at least 20 characters";
    } else {
        messageError.style.display = "none";
        Emailmessage.setCustomValidity("");
    }
};




function createMessage() {
    const submitProgress = document.getElementById("submit_progress");
    submitProgress.style.display = 'block';
    const url = "https://kepicmail.herokuapp.com/api/v2/messages";
    const newMessage = {
        reciever: reciever.value,
        subject: subject.value,
        message: message.value,

    };
    console.log('hrrtyugihft')
    console.log(newMessage)
    let token = localStorage.getItem("token");
    fetch(url, {
        method: "POST",
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newMessage),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 400) {
                submitProgress.style.display = 'hide';

                displayError(data.error);

            } else if (data.status === 401) {
                displayError(data.error);
                window.setTimeout(function () {
                    window.location.replace("../index.html");
                }, 5000);


            } else if (data.status === 201) {
                //on success
                submitProgress.style.display = 'hide';

                let successMsg = data["data"][0]["success"];
                document.getElementById('success_msg').style.display = "block";
                document.getElementById('success_msg').innerHTML = "message sent Successfully!";
                window.setTimeout(function () {
                    window.location.replace("./user_dashboard.html");
                }, 1000);;

            }

        })
        .catch((error) => console.log(error));

}
function logout() {
    localStorage.removeItem("token");
}



