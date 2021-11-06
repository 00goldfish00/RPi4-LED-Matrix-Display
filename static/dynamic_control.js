/**
 *  A bunch of functions that interact with the DOM and syncronize values between inputs. 
 */
function changeRed(value) {
    document.getElementById('redLabel').innerHTML = value;
    changeAll();
}
function changeGreen(value) {
    document.getElementById('greenLabel').innerHTML = value;
    changeAll();
}
function changeBlue(value) {
    document.getElementById('blueLabel').innerHTML = value;
    changeAll();
}
function changeColor(value) {
    var rgb = w3color(value).toRgb();
    document.getElementById("red1").value = rgb.r;
    document.getElementById("green1").value = rgb.g;
    document.getElementById("blue1").value = rgb.b;

    document.getElementById('redLabel').innerHTML = rgb.r;
    document.getElementById('greenLabel').innerHTML = rgb.g;
    document.getElementById('blueLabel').innerHTML = rgb.b;
    changeAll();
}
function changeAll() {
    var r = document.getElementById('redLabel').innerHTML;
    var g = document.getElementById('greenLabel').innerHTML;
    var b = document.getElementById('blueLabel').innerHTML;
    var colorObj = w3color("rgb(" + r + "," + g + "," + b + ")");
    document.getElementById('color1').value = colorObj.toHexString();
    var btn = document.getElementById('submitBtn');
    btn.style.backgroundColor = "rgb(" + r + "," + g + "," + b + ")";
    if (!colorObj.isDark()) {
        btn.style.color = "var(--bs-gray-dark";
    } else {
        btn.style.color = "#fff";
    }
    document.getElementById('colorTxt').innerHTML = "rgb(" + r + ", " + g + ", " + b + ")";
    document.getElementById('colorTxtHex').innerHTML = colorObj.toHexString();
}