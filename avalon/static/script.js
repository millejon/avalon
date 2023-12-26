// Show playlist menu when user clicks on button.
function displayPlaylists(song) {
    var elementId = "playlists_list_" + song
    document.getElementById(elementId).classList.toggle("show");
}

// Close playlist menu if user clicks outside of it.
window.onclick = function(event) {
    if (!event.target.matches('.display_playlist_button')) {
        var playlistMenus = document.getElementsByClassName("playlists_list");
        var index;
        for (index = 0; index < playlistMenus.length; index++) {
            var openMenu = playlistMenus[index];
            if (openMenu.classList.contains('show')) {
                openMenu.classList.remove('show');
            }
        }
    }
}
