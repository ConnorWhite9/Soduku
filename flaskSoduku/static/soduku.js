

window.onload = function(){
    let form = document.getElementsByClassName("sodukuForm")[0]; 
    let check = document.getElementById('check')
    let merged = document.getElementsByClassName("identifier");
    console.log(merged);
    check.addEventListener("click", function () {
        console.log("hello my fellow earthlings what a wonderful day we have here as we now approach the apex of the year")
        checkVars = {}
        for (let i = 0; i < merged.length; i++ ) {
            
            if (merged[i].tagName == "TD") { 
                    var id = merged[i].id;
                    checkVars[id] = merged[i].innerHTML
            }else{
                if (merged[i].value.trim().length === 0) {   
                    alert("Complete Soduku Before Attempting To Check")
                    console.log(merged[i])
                    return;  
                }else{
                    var id = merged[i].id;
                    checkVars[id] = merged[i].value
                }
            }
        }
        var entry = {
            checkVars: checkVars
        };

        
        
        fetch(`${window.origin}/sodukuPage`, {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(entry),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json",
                "X-CSRF-Token": csrf_token,
            })
        })
        .then(function(response) {
            if (response.status !== 200){
                console.log("Failure")
                return ;
            }
            response.json().then(function (data) {
                console.log(data)
                const myModal = new bootstrap.Modal('#modal23');
                myModal.show()
                let message = document.getElementById("message");
                let modalFooter = document.getElementById("modal-footer");
                let modalHeader = document.getElementById("modal-header");
                let modalTitle = document.getElementById("modalTitle");
                if (data['code'] == "green"){
                    timer = false
                    message.style.color = "green";
                    message.innerHTML = `Congratulations You Successfully Completed This Soduku! Your Completion Time Was ${minString} Minutes And ${secString} seconds.`;
                    modalFooter.style.backgroundColor = "green";
                    modalHeader.style.backgroundColor = "green";
                    modalTitle.innerHTML = "Correct!";
                
                }
                else {
                    message.style.color = "red"
                    message.innerHTML = "Uh Oh, It Appears Some of Your Responses Were Incorrect. Check Your Work Over And Try Submitting Again."
                    modalFooter.style.backgroundColor = "red";
                    modalHeader.style.backgroundColor = "red";
                    modalTitle.innerHTML = "Incorrect!";
                
                }
            })
        })
    });
}




/* for (element in allElements) {
    if (element.tagName == "input"){
        console.log("top")
        if (element.value.trim().length === 0) {
            
            alert("Complete Soduku Before Attempting To Check")
            return;
            
        } else {
            var id = element.id;
            checkVars[id] = element.value
        }
}};
$.ajax({
    type: "POST",
    url: "/sodukuPage",
    contentType: "application/json",
    data: {"checkVars": 1},
})
.done(function(data){
    button = document.getElementsByTagName("button")
    button.style.backgroundColor = "red";
}); */ 