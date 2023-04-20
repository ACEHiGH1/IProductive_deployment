function completeTask(taskPk) {
    document.getElementById(`completedStatusTask${taskPk}`).style.display = "block";
    document.getElementById(`incompletedStatusTask${taskPk}`).style.display = "none";

    document.getElementById(`completeButtonTask${taskPk}`).style.display = "none";
    document.getElementById(`incompleteButtonTask${taskPk}`).style.display = "block";

    fetch(`completeTask/${taskPk}`)
        .then(response => response.json())
        .then(currentDay => {
            console.log(currentDay);

            document.getElementById('dailyPoints').innerHTML = `Daily Points: ${currentDay.dailyPoints}`;
        })
}

function incompleteTask(taskPk, taskPoints, dailyPoints) {
    document.getElementById(`completedStatusTask${taskPk}`).style.display = "none";
    document.getElementById(`incompletedStatusTask${taskPk}`).style.display = "block";

    document.getElementById(`completeButtonTask${taskPk}`).style.display = "block";
    document.getElementById(`incompleteButtonTask${taskPk}`).style.display = "none";

    fetch(`incompleteTask/${taskPk}`)
        .then(response => response.json())
        .then(currentDay => {
            console.log(currentDay);

            document.getElementById('dailyPoints').innerHTML = `Daily Points: ${currentDay.dailyPoints}`;
        })
}

function completeHobby(hobbyPk) {
    document.getElementById(`completedStatusHobby${hobbyPk}`).style.display = "block";
    document.getElementById(`incompletedStatusHobby${hobbyPk}`).style.display = "none";

    document.getElementById(`completeButtonHobby${hobbyPk}`).style.display = "none";
    document.getElementById(`incompleteButtonHobby${hobbyPk}`).style.display = "block";

    fetch(`completeHobby/${hobbyPk}`)
        .then(response => response.json())
        .then(currentDay => {
            console.log(currentDay);

            document.getElementById('dailyPoints').innerHTML = `Daily Points: ${currentDay.dailyPoints}`;
        })
}

function incompleteHobby(hobbyPk) {
    document.getElementById(`completedStatusHobby${hobbyPk}`).style.display = "none";
    document.getElementById(`incompletedStatusHobby${hobbyPk}`).style.display = "block";

    document.getElementById(`completeButtonHobby${hobbyPk}`).style.display = "block";
    document.getElementById(`incompleteButtonHobby${hobbyPk}`).style.display = "none";

    fetch(`incompleteHobby/${hobbyPk}`)
        .then(response => response.json())
        .then(currentDay => {
            console.log(currentDay);

            document.getElementById('dailyPoints').innerHTML = `Daily Points: ${currentDay.dailyPoints}`;
        })
}

function deleteTask(taskPk) {
    task = document.getElementById(`task${taskPk}`);
    task.parentNode.removeChild(task);

    fetch(`deleteTask/${taskPk}`)
        .then(response => response.json())
        .then(currentDay => {
            document.getElementById('dailyPoints').innerHTML = `Daily Points: ${currentDay.dailyPoints}`;
        })
}

function deleteHobby(hobbyPk) {
    hobby = document.getElementById(`hobby${hobbyPk}`);
    hobby.parentNode.removeChild(hobby);

    fetch(`deleteHobby/${hobbyPk}`)
        .then(response => response.json())
        .then(currentDay => {
            document.getElementById('dailyPoints').innerHTML = `Daily Points: ${currentDay.dailyPoints}`;
        })
}

function showFriends() {
    document.getElementById("friends").style.display = "block";
    document.getElementById("showFriendsButton").style.display = "none";
    document.getElementById("hideFriendsButton").style.display = "block";

}

function hideFriends() {
    document.getElementById("friends").style.display = "none";
    document.getElementById("showFriendsButton").style.display = "block";
    document.getElementById("hideFriendsButton").style.display = "none";
}

function searchUsername() {
    username = document.getElementById("usernameSearched").value;
    fetch(`view/${username}`, {
        method: 'GET'
    });
}

function showNewTaskForm() {
    document.getElementById("createNewTask").style.display = "block";
    document.getElementById("showNewTaskFormButton").style.display = "none";
}

function hideNewTaskForm() {
    document.getElementById("createNewTask").style.display = "none";
    document.getElementById("showNewTaskFormButton").style.display = "block";
}

function showNewHobbyForm() {
    document.getElementById("createNewHobby").style.display = "block";
    document.getElementById("showNewHobbyFormButton").style.display = "none";
}

function hideNewHobbyForm() {
    document.getElementById("createNewHobby").style.display = "none";
    document.getElementById("showNewHobbyFormButton").style.display = "block";
}

function viewDay(dayPk) {
    document.getElementById(`day${dayPk}details`).style.display = "block";
    document.getElementById(`closeDay${dayPk}`).style.display = "block";
    document.getElementById(`viewDay${dayPk}`).style.display = "none";
}

function closeDay(dayPk) {
    document.getElementById(`day${dayPk}details`).style.display = "none";
    document.getElementById(`closeDay${dayPk}`).style.display = "none";
    document.getElementById(`viewDay${dayPk}`).style.display = "block";
}

function removeFriend(username) {
    document.getElementById("removeFriendButton").style.display = "none";
    document.getElementById("addFriendButton").style.display = "block";
    document.getElementById("otherUserDaysOverview").style.display = "none";

    fetch(`/removeFriend/${username}`)
        .then(response => response.json())
        .then(message => {
            console.log(message);
        })
}

function addFriend(username) {
    document.getElementById("cancelFriendRequest").style.display = "block";
    document.getElementById("addFriendButton").style.display = "none";

    fetch(`/addFriend/${username}`)
        .then(response => response.json())
        .then(message => {
            console.log(message);
        })
}

function removeFriendRequest(username) {
    document.getElementById("cancelFriendRequest").style.display = "none";
    document.getElementById("addFriendButton").style.display = "block";

    fetch(`/cancelFriendRequest/${username}`)
        .then(response => response.json())
        .then(message => {
            console.log(message);
        })
}

function dropDownFunction() {
    if (document.getElementById("friendRequestDropdown").style.display == "block") {
        document.getElementById("friendRequestDropdown").style.display = "none";
    } else {
        document.getElementById("friendRequestDropdown").style.display = "block";
    }
}

function acceptFriendRequest(username) {
    document.getElementById(`accept${username}`).disabled = true;
    document.getElementById(`accept${username}`).innerHTML = "You are now friends.";
    document.getElementById(`decline${username}`).style.display = "none";

    document.getElementById(`accept${username}profile`).disabled = true;
    document.getElementById(`accept${username}profile`).innerHTML = "You are now friends.";
    document.getElementById(`decline${username}profile`).style.display = "none";

    document.getElementById("otherUserDaysOverview").style.display = "block";
    document.getElementById("notFriendsActivity").innerHTML = "Refresh the page to see the posts.";
    console.log(username);

    fetch(`/acceptFriendRequest/${username}`)
        .then(response => response.json())
        .then(message => {
            console.log(message)
        })
}

function declineFriendRequest(username) {
    document.getElementById(`decline${username}`).disabled = true;
    document.getElementById(`decline${username}`).innerHTML = "Declined";
    document.getElementById(`accept${username}`).style.display = "none";

    document.getElementById(`decline${username}profile`).disabled = true;
    document.getElementById(`decline${username}profile`).innerHTML = "Declined";
    document.getElementById(`accept${username}profile`).style.display = "none";

    fetch(`/declineFriendRequest/${username}`)
        .then(response => response.json())
        .then(message => {
            console.log(message)
        })
}

function acceptFriendRequestProfile(username) {
    document.getElementById(`accept${username}profile`).disabled = true;
    document.getElementById(`accept${username}profile`).innerHTML = "You are now friends.";
    document.getElementById(`decline${username}profile`).style.display = "none";

    document.getElementById("otherUserDaysOverview").style.display = "block";

    console.log(username);

    fetch(`/acceptFriendRequest/${username}`)
        .then(response => response.json())
        .then(message => {
            console.log(message)
        })
}

function declineFriendRequestProfile(username) {
    document.getElementById(`decline${username}profile`).disabled = true;
    document.getElementById(`decline${username}profile`).innerHTML = "Declined";
    document.getElementById(`accept${username}profile`).style.display = "none";

    fetch(`/declineFriendRequest/${username}`)
        .then(response => response.json())
        .then(message => {
            console.log(message)
        })
}

