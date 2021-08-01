document.addEventListener('DOMContentLoaded', function() {

    // Obtain value for current user, current URL and current URL path
    const currentUser = document.querySelector('#allPosts').getAttribute('value');
    var currentURL = location.pathname;
    const path = currentURL.split("/");

    if (String(path[2]) !== currentUser) {
        document.querySelector('#follow-btn').addEventListener('click', () => follow());
        document.querySelector('#follow-btn').onmouseover = document.querySelector('#follow-btn').onmouseout = follow_hover;
    };
})

function follow() {

    const username = document.querySelector('#follow-btn').getAttribute('value');

    fetch(`/update_userProfile/${username}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(currentUser => {
        console.log(currentUser);

        // Set the selected follow button as variable
        const follow_btn = document.querySelector(`#follow-btn`);

        // Change the follow button style effect based on the following status
        if (currentUser.error) {
            // Change to Followed button style 
            follow_btn.classList.remove('unfollowed');
            follow_btn.classList.add('followed');
            follow_btn.innerHTML = 'Following';
        } else if (currentUser.following.includes(username)) {
            // Change to Unfollowed button style 
            follow_btn.classList.remove('followed');
            follow_btn.classList.add('unfollowed');
            follow_btn.style.backgroundColor = "white";
            follow_btn.style.color = "#4166f5";
            follow_btn.innerHTML = 'Follow';
        } else if (!currentUser.following.includes(username)) {
            // Change to Followed button style 
            follow_btn.classList.remove('unfollowed');
            follow_btn.classList.add('followed');
            follow_btn.innerHTML = 'Following';
        };

        // Update following status in the server
        fetch(`/update_userProfile/${username}`, {
            method: 'PUT',
            body: JSON.stringify({
                followButton_triggered: true
            })
        });
    })
}

function follow_hover(event) {
    const username = document.querySelector('#follow-btn').getAttribute('value');

    fetch(`/update_userProfile/${username}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(currentUser => {
        console.log(currentUser);

        // Change the follow button style effect based on the following status
        if (currentUser.error) {
            if (event.type == 'mouseover') {
                // Change to Followed button style 
                event.target.style.backgroundColor = "#4166f5";
                event.target.style.color = "white";
            } else if (event.type == 'mouseout') {
                event.target.style.backgroundColor = "white";
                event.target.style.color = "#4166f5";
            };
        } else if (currentUser.following.includes(username)) {
            if (event.type == 'mouseover') {
                // Change to Unfollowed hover effect
                event.target.style.backgroundColor = "rgb(160, 0, 0)";
                event.target.innerHTML = 'Unfollow';
            } else if (event.type == 'mouseout') {
                event.target.style.backgroundColor = "#4166f5";
                event.target.innerHTML = 'Following';
            };
        } else if (!currentUser.following.includes(username)) {
            if (event.type == 'mouseover') {
                // Change to Followed button style 
                event.target.style.backgroundColor = "#4166f5";
                event.target.style.color = "white";
            } else if (event.type == 'mouseout') {
                event.target.style.backgroundColor = "white";
                event.target.style.color = "#4166f5";
            };
        };
    })
}
