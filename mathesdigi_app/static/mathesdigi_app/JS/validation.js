/** This function is designed to validate a single input field with the ID kids_answer_1.
 *  The function checks if the input field is empty and if so, adds a CSS class input_field_shake
 *  to create a shaking effect to draw the user's attention.
 *  It then removes this class after a delay of 1 second using setTimeout().*/
function validateForm_singleAnswer() {
    const kids_answer = document.getElementById("kids_answer_1").value;
    if (kids_answer.trim() === "") {
        document.getElementById("kids_answer_1").classList.add("input_field_shake");
        setTimeout(function () {
            document.getElementById("kids_answer_1").classList.remove("input_field_shake");
        }, 1000);
        return false;
    } else {
        document.getElementById("kids_answer_1").classList.remove("input_field_shake");
        return true;
    }
}