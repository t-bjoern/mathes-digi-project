let last_clicked_input_field_id

/**This code listens for the DOM to load. After that it adds EventListener for clicking, keyboard-inputs.*/
document.addEventListener("DOMContentLoaded", function () {
    const inputFields = document.querySelectorAll("input[type='text']");
    inputFields.forEach(function (inputField) {
        inputField.addEventListener("click", function () {
            last_clicked_input_field_id = this.id;
        });
        inputField.addEventListener("keydown", keyboard_add_number);
        inputField.addEventListener("touchstart", function () {
            last_clicked_input_field_id = this.id;
        })
    });

    // Catch Touch-Move-Event (prevent scrolling on tablets)
    document.addEventListener("touchmove", function (event) {
        event.preventDefault();
    }, {passive: false});
});

/** Action for keyboard-input
 *  Only keys 0-9 and Backspace are allowed. Only three digits can be written.
 */
function keyboard_add_number(event) {
    if (event.key >= "0" && event.key <= "9" && this.value.length < 3) {
    } else if (event.key === "Backspace") {
    } else {
        event.preventDefault();
    }
}

/** Action for number-buttons
 * The value of the clicked button is appended to the text of the last clicked target. Only three digits are allowed.
 * If no input-field had been clicked it will automatically start writing in the first field.
 *
 * The information about the clicked buttons is stored in stat.*/
function buttons_add_number(stat) {
    if (typeof last_clicked_input_field_id === "undefined") {
        last_clicked_input_field_id = "kids_answer_1"
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