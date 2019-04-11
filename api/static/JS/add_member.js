function displayError(dataArray) {

    for (let key in dataArray) {

        if ({}.hasOwnProperty.call(dataArray, key)) {
            let fieldError = document.getElementById(key + "-error");
            fieldError.style.display = "block";
            fieldError.innerHTML = dataArray[key];
        }
    }
}


const Newuser_id = document.getElementById("userid");


Newuser_id .onkeyup = function () {
    const useridError = document.getElementById('userid-error');
   
    
    if (Newuserid !==isNaN()) {
        useridError.style.display = "block";
        useridError.innerHTML = "user Id must be a number.";
        Newuserid.setCustomValidity("Invalid userId provided.");

    } else {
        useridError.style.display = "none";
        Newuserid.setCustomValidity("");

    }

};



function addMember() {
    const submitProgress = document.getElementById("submit_progress");
    submitProgress.style.display = 'block';
    
    let userid = document.getElementById("myInput")
    const url = "/api/v2/groups/";
    const newMember = {
        userid: userid.value,

    };
    console.log(newMember)
    let token = localStorage.getItem("token");
    fetch(url, {
        method: "POST",
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newMember),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 400) {
                submitProgress.style.display = 'hide';
                displayError(data.error);
                window.setTimeout(function () {
                    window.location.replace("/Admin.html");
                }, 5000);

            } else if (data.status === 401) {
                displayError(data.error);
                window.setTimeout(function () {
                    window.location.replace("/");
                }, 5000);

            } else if (data.status === 201) {
                //on success
                submitProgress.style.display = 'hide';

                let successMsg = data["data"][0]["success"];
                document.getElementById('success_msg').style.display = "block";
                document.getElementById('success_msg').innerHTML = "member added Successfully!";
                window.setTimeout(function () {
                    window.location.replace("/group.html");
                }, 5000);;

            }

        })
        .catch((error) => console.log(error));

}
