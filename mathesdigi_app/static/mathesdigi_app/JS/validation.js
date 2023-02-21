/** This function is designed to validate a single input field with the ID kids_answer_input_field_1.
 *  The function checks if the input field is empty and if so, adds a CSS class input_field_shake
 *  to create a shaking effect to draw the user's attention.
 *  It then removes this class after a delay of 1 second using setTimeout().*/
function validateForm_singleAnswer() {
    const kids_answer_input_field = document.getElementById("kids_answer_1");
    if (kids_answer_input_field.value.trim() === "") {
        kids_answer_input_field.classList.add("input_field_shake");
        kids_answer_input_field.classList.remove("input_field_shake");
        setTimeout(function () {
            kids_answer_input_field.classList.remove("input_field_shake");
        }, 800);
        return false;
    } else {
        kids_answer_input_field.classList.remove("input_field_shake");
        return true;
    }
}

function validateForm_example_singleAnswer(solution) {
    validateForm_singleAnswer()
    const kids_answer_input_field = document.getElementById("kids_answer_1");

    if (kids_answer_input_field.value === solution) {
        kids_answer_input_field.style.color = 'green';
        setTimeout(function () {
            document.getElementById("myform").submit();
        }, 3000);
    } else {
        kids_answer_input_field.style.color = 'red';
        setTimeout(function () {
            kids_answer_input_field.value = solution;
            kids_answer_input_field.style.color = 'green';
        }, 1000);
        setTimeout(function () {
            document.getElementById("myform").submit();
        }, 4000);
    }
    return false;
}