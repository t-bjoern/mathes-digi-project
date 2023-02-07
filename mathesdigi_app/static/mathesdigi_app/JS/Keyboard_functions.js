/*This code listens for the DOM to load and then sets a reference to an input field with the id "antwort1".
It then sets an event listener on that input field for the "keydown" event.

The function attached to the event listener checks the pressed key, if it is a number between 0 and 9 and
the length of the input value is less than 3, it allows the key press to go through. If the pressed key is
the backspace key, it also allows the key press to go through. In all other cases, it prevents the default
behavior of the key press.*/
document.addEventListener("DOMContentLoaded", function () {
    let inputField = document.getElementById("antwort1");
    inputField.addEventListener("keydown", function (event) {
        if (event.key >= "0" && event.key <= "9" && this.value.length < 3) {
        } else if (event.key === "Backspace") {
        } else {
            event.preventDefault();
        }
    });
});

