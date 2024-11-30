

function logout() {
    const baseUrl = `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}`;
    const apiUrl = `${baseUrl}/auth/logout`;

    const requestOptions = {
        method: "POST",
        redirect: "follow"
      };
      
    fetch(apiUrl, requestOptions)
    .then((response) => {
        if (response.ok) {
            window.location.href = `${baseUrl}/login`;
        } else {
            console.error(response);
        }
    })
    .then((result) => console.log(result))
    .catch((error) => console.error(error));
}