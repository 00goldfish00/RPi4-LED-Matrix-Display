/**
 *  A bunch of functions that interact with the DOM and syncronize values between inputs. 
 */
function changeColor(value) {
    var rgb = w3color(value).toRgb();
    // When the color picker is changed,
    // convert the hex value to RGB and set the slider values.
    document.getElementById("red1").value = rgb.r;
    document.getElementById("green1").value = rgb.g;
    document.getElementById("blue1").value = rgb.b;

    // Also update all labels
    changeAll();
}
function changeAll() {
    // Get current R G and B values from the sliders
    var r = document.getElementById("red1").value;
    var g = document.getElementById("green1").value;
    var b = document.getElementById("blue1").value;
    // Update labels
    document.getElementById('redLabel').innerHTML = r;
    document.getElementById('greenLabel').innerHTML = g;
    document.getElementById('blueLabel').innerHTML = b;
    // Create a color object using the w3color library
    var colorObj = w3color("rgb(" + r + "," + g + "," + b + ")");
    // Set color picker value
    document.getElementById('color1').value = colorObj.toHexString();

    // Set hex label text
    var hexColor = colorObj.toHexString();
    if(hexColor == "#000000"){
        document.getElementById('colorTxtHex').innerHTML = "OFF";
    } else {
        document.getElementById('colorTxtHex').innerHTML = colorObj.toHexString();
    }

    // Set rgb color text
    document.getElementById('colorTxt').innerHTML = colorObj.toRgbString();

    // Change color of submit button to match the selected color
    var btn = document.getElementById('submitBtn');
    btn.style.backgroundColor = colorObj.toRgbString()
    if (!colorObj.isDark()) {
        // Con
        btn.style.color = "var(--bs-gray-dark)";
    } else {
        btn.style.color = "var(--bs-white)";
    }

    document.getElementById("colorSwatch").style.backgroundColor = colorObj.toRgbString();

}