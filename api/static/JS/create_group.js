function displayError(dataArray) {

    for (let key in dataArray) {

        if ({}.hasOwnProperty.call(dataArray, key)) {
            let fieldError = document.getElementById(key + "-error");
            fieldError.style.display = "block";
            fieldError.innerHTML = dataArray[key];
        }
    }
}


const Newgroup_name = document.getElementById("group_name");


Newgroup_name.onkeyup = function () {
    const group_nameError = document.getElementById('group_name-error');
    
    if (Newgroup_name == "") {
        group_nameError.style.display = "block";
        group_nameError.innerHTML = "group name must not contain space.";
        Newgroup_name.setCustomValidity("Invalid group name provided.");

    } else if (Newgroup_name.value.length < 4) {
        group_nameError.style.display = "block";
        group_nameError.innerHTML = "group_name must contain atleast 4 characters";
        Newgroup_name.setCustomValidity("Invalid group name provided.");


    } else if (Newgroup_name.value.length > 100) {
        group_nameError.style.display = "block";
        group_nameError.innerHTML = "group_name can not contain more than 100 characters";
        Newgroup_name.setCustomValidity("Invalid group name provided.");

    } else {
        group_nameError.style.display = "none";
        Newgroup_name.setCustomValidity("");

    }

};



function createGroup() {
    const submitProgress = document.getElementById("submit_progress");
    submitProgress.style.display = 'block';
    
    let group_name = document.getElementById("myInput")
    const url = "/api/v2/groups";
    const newGroup = {
        group_name: group_name.value,

    };
    console.log(newGroup)
    let token = localStorage.getItem("token");
    fetch(url, {
        method: "POST",
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newGroup),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 400) {
                submitProgress.style.display = 'hide';
                displayError(data.error);
                window.setTimeout(function () {
                    window.location.replace("/group.html");
                }, 5000);

            } else if (data.status === 401) {
                displayError(data.error);
                window.setTimeout(function () {
                    window.location.replace("../index.html");
                }, 1000);


            } else if (data.status === 201) {
                //on success
                submitProgress.style.display = 'hide';

                let successMsg = data["data"][0]["success"];
                document.getElementById('success_msg').style.display = "block";
                document.getElementById('success_msg').innerHTML = "Group created Successfully!";
                window.setTimeout(function () {
                    window.location.replace("/group.html");
                }, 5000);;

            }

        })
        .catch((error) => console.log(error));

}
function logout() {
    localStorage.removeItem("token");
}
