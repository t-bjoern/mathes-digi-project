/** This function checks if the input field is empty and if so, adds a CSS class input_field_shake
 *  to create a shaking effect to draw the user's attention.
 *  It then removes this class after a delay of 1 second using setTimeout().*/
function checkForm_singleAnswer() {
    const kids_answer_input_field = document.getElementById("kids_answer_1");
    if (kids_answer_input_field.value.trim() === "") {
        kids_answer_input_field.classList.add("input_field_shake");
        setTimeout(function () {
            kids_answer_input_field.classList.remove("input_field_shake");
        }, 800);
        return false;
    }
}

/** This function is called for each example. The input-field shakes if it is empty. Otherwise, it changes the
 * color of the answer to red or green. For wrong answers it shows the correct solution.
 * The page redirects (submits the form) after a few seconds.
 * */
function checkForm_example_singleAnswer(solution) {
    const kids_answer_input_field = document.getElementById("kids_answer_1");
    if (kids_answer_input_field.value.trim() === "") {
        kids_answer_input_field.classList.add("input_field_shake");
        setTimeout(function () {
            kids_answer_input_field.classList.remove("input_field_shake");
        }, 800);
    } else if (kids_answer_input_field.value === solution) {
        kids_answer_input_field.style.color = 'green';
        setTimeout(function () {
            document.getElementById("example_form").submit();
        }, 2000);
    } else {
        kids_answer_input_field.style.color = 'red';
        setTimeout(function () {
            kids_answer_input_field.value = solution;
            kids_answer_input_field.style.color = 'green';
        }, 1000);
        setTimeout(function () {
            document.getElementById("example_form").submit();
        }, 3000);
    }
    return false;
}

/** Handling for Drag and Drop tasks.
 * Adds shaking to empty answer-fields and sets the given answers into a hidden
 * input-field for submitting.
 * Divs are needed for allowing images and text in the same field. */
function checkForm_dragAndDrop() {
    const answer_divs = document.querySelectorAll('.answer');
    let kids_answer_list = [];
    let shake_list = [];
    answer_divs.forEach(function (single_answer) {
        if (single_answer.innerHTML.trim() === '') {
            shake_list.push(single_answer.id);
        } else if (single_answer.innerHTML.includes('<img')) {
            let imgElement = single_answer.querySelector('img');
            let imgID = imgElement.getAttribute('id');
            kids_answer_list.push(imgID);
        } else {
            kids_answer_list.push(single_answer.textContent.trim());
        }
    });

    if (shake_list.length !== 0) {
        shake_list.forEach(function (shake_element) {
            let shake_field = document.getElementById(shake_element);
            shake_field.classList.add("input_field_shake");
            setTimeout(function () {
                shake_field.classList.remove("input_field_shake");
            }, 800);
            return false;
        });
    } else {
        const input_field = document.getElementById('answers_collected');
        input_field.value = kids_answer_list;
        return true;
    }
    return false;
}