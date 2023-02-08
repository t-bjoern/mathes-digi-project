let last_clicked_input_field_id

/**This code listens for the DOM to load and then sets a reference for each input-field.
 It then sets an event listener on that input field for the "keydown" and "click" event.*/
document.addEventListener("DOMContentLoaded", function () {
    let inputFields = document.querySelectorAll("input[type='text']");

    inputFields.forEach(function (inputField) {
        inputField.addEventListener("click", getID);
        inputField.addEventListener("keydown", keyboard_add_number);
    });
});

/**
 * The function attached to the event listener sets the id of the clicked input field to lastclickedinputfield_id.
 */
function getID() {
    last_clicked_input_field_id = this.id;
}

/** Action for keyboard-input
 The function attached to the event listener checks the pressed key, if it is a number between 0 and 9 and
 the length of the input value is less than 3, it allows the key press to go through. If the pressed key is
 the backspace key, it also allows the key press to go through. In all other cases, it prevents the default
 behavior of the key press.*/
function keyboard_add_number(event) {
    if (event.key >= "0" && event.key <= "9" && this.value.length < 3) {
    } else if (event.key === "Backspace") {
    } else {
        event.preventDefault();
    }
}

/** Action for number-buttons
 The information about the clicked buttons is stored in stat.
 If no input-field has been clicked, the default-inputfield "antwort1" will be selected.
 Otherwise if the user already clicked an input-field the id of that field will be stored in lastclickedinputfield_id.
 If the clicked button id is "p_delete" the input-field is going to be set to ''. If the value of the input-field has
 fewer than 3 digits, the function appends the value of the clicked button (stat) to the target (input-field).*/
function buttons_add_number(stat) {
    if (typeof last_clicked_input_field_id === "undefined") {
        last_clicked_input_field_id = "antwort1"
    }
    let target = document.getElementById(last_clicked_input_field_id);

    if (stat.id === 'p_delete') {
        target.value = ''
    } else {
        if (target.value.length < 3) {
            target.value = target.value + stat.value;
        }
    }
}