document.addEventListener('DOMContentLoaded', function() {

    const currentUser = document.querySelector('#allPosts').getAttribute('value');
    var currentURL = location.pathname;
    const path = currentURL.split("/");

    if (String(currentUser) !== "") {
      if (String(currentURL) === "/" || String(path[1]) === "following") {
        document.querySelector('#post-btn').addEventListener('click', (event) => createPost(event));
      };
    }

    document.querySelectorAll('.edit-btn').forEach(function(button) {
        button.onclick = function () {

          const post_id = button.dataset.id;
          const content_value = document.querySelector(`#post-content-body-id${post_id}`).innerHTML

          document.querySelectorAll(`.edit-btn`).forEach(function(button) {
            button.style.display = "none";
          });
          
          const edit_post = document.querySelector(`#post-content-id${post_id}`)
          edit_post.innerHTML = `<form id=edit-form${post_id}>
                                    <textarea class="form-control form-post-style my-3 p-2 px-4" id="post-edit-data" placeholder="Edit you post" rows="2">${content_value}</textarea>
                                    <div class="d-flex flex-row flex-row-reverse">
                                      <button id="save-btn" class="edit-btn">Save</button>
                                    </div>
                                  </form>`;

          document.querySelector(`#edit-form${post_id}`).addEventListener('submit', (event) => savePost(event, post_id, edit_post));
        }
    });
});

function createPost(event) {

    event.preventDefault();

    const content = document.querySelector('#post-body-data').value;

    fetch('/create_post', {
        method: 'POST',
        body: JSON.stringify({
            content: content,
        })
    })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
      const message = Object.values(result);
      if (result.error) {
        document.querySelector('#alert-msg').innerHTML = `<div class="alert alert-danger d-flex align-items-center alert-dismissable fade show" role="alert"><svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg><div>${message}</div><button type="button" class="btn-close" style="margin-left: auto; margin-right: 5px;" data-bs-dismiss="alert" aria-label="Close"></button></div>`;
      }
      else {
        window.location.replace('/');
      }
    });
}

function savePost(event, post_id, edit_post) {

    event.preventDefault();
  
    const edit_content = document.querySelector('#post-edit-data').value;

    fetch(`/update_post/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          edit_content: edit_content,
        })
    })
    .then(response => response.json())
    .then(result => {
      // Print result
      if(result.error) {
        console.log(result);
      } else {
        console.log(result);
        edit_post.innerHTML = `<p id="post-content-body-id${post_id}" class="post-body my-0 mx-1">${edit_content}</p>`;
        document.querySelectorAll('.edit-btn').forEach(function(button) {
          button.style.display = "block";
        });
      }
    });
}
