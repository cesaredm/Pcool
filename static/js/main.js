var http;
if (window.XMLHttpRequest) {
    http = new XMLHttpRequest();
} else {
    http = new ActiveXObject("Microsoft.XMLHTTP");
}

http.onreadystatechange = function()
{
    if (this.readyState === 4 && this.status === 200) {
        alert("Listo..!");
    }
}
http.open("GET", "servidor.php", true);
http.send();


