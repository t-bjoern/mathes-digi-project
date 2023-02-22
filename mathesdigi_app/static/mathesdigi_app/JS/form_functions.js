const shake_duration = 800;
const red_to_green_duration = 1000;
const correct_forward = 2000;
const wrong_forward = 3000;


/** This function checks if the input field is empty and if so, adds a CSS class input_field_shake
 *  to create a shaking effect to draw the user's attention.
 *  It then removes this class after a delay of 1 second using setTimeout().*/
function checkForm_singleAnswer() {
    const kids_answer_input_field = document.getElementById("kids_answer_1");
    if (kids_answer_input_field.value.trim() === "") {
        kids_answer_input_field.classList.add("input_field_shake");
        setTimeout(function () {
            kids_answer_input_field.classList.remove("input_field_shake");
        }, shake_duration);
        return false;
    } else {
        return true;
    }
}

/** This function is called for each single_example. The input-field shakes if it is empty. Otherwise, it changes the
 * color of the answer to red or green. For wrong answers it shows the correct solution.
 * The page redirects (submits the form) after a few seconds.
 * */
function checkForm_example_singleAnswer(solution) {
    const kids_answer_input_field = document.getElementById("kids_answer_1");
    if (kids_answer_input_field.value.trim() === "") {
        kids_answer_input_field.classList.add("input_field_shake");
        setTimeout(function () {
            kids_answer_input_field.classList.remove("input_field_shake");
        }, shake_duration);
    } else if (kids_answer_input_field.value === solution) {
        kids_answer_input_field.style.color = 'green';
        setTimeout(function () {
            document.getElementById("example_form").submit();
        }, correct_forward);
    } else {
        kids_answer_input_field.style.color = 'red';
        setTimeout(function () {
            kids_answer_input_field.value = solution;
            kids_answer_input_field.style.color = 'green';
        }, red_to_green_duration);
        setTimeout(function () {
            document.getElementById("example_form").submit();
        }, wrong_forward);
    }
    return false;
}

/** Handling for Drag and Drop tasks.
 * Adds shaking to empty answer-fields and sets the given answers into a hidden input-field for submitting.
 * Divs are needed for allowing images and text in the same field. */
function checkForm_dragAndDrop() {
    const answer_divs = document.querySelectorAll('.answer');
    let kids_answer_list = [];
    let shake = false;


    answer_divs.forEach(function (single_answer) {
        // shake-Handling
        if (single_answer.innerHTML.trim() === '') {
            single_answer.classList.add("input_field_shake");
            setTimeout(function () {
                single_answer.classList.remove("input_field_shake");
            }, shake_duration);
            shake = true;
        }
        // collecting kids_answers
        else if (single_answer.innerHTML.includes('<img')) {
            let imgElement = single_answer.querySelector('img');
            let imgID = imgElement.getAttribute('id');
            kids_answer_list.push(imgID);
        } else {
            kids_answer_list.push(single_answer.textContent.trim());
        }
    });

    // set collected_answers in hidden input-field and submit form
    if (!shake) {
        const input_field = document.getElementById('answers_collected');
        input_field.value = kids_answer_list;
        return true;
    }
    return false;
}

/** Handling for examples with Drag and Drop.
 * Adds shaking to empty answer-fields.
 * If all answers where given, the images are exchanged against text in red or green and on the same time tey are reset
 * to the task-pics field. After that the wrong answer are getting corrected and set to green. Then the page is redirected
 * to the next task (submit the form)
 * Divs are needed for allowing images and text in the same field. */
function checkForm_example_dragAndDrop(solution) {
    const answer_divs = document.querySelectorAll('.answer');
    const task_pics = document.getElementById('task_pics');
    let shake = false;

    // shake-Handling
    answer_divs.forEach(function (single_answer) {
        if (single_answer.innerHTML.trim() === '') {
            single_answer.classList.add("input_field_shake");
            setTimeout(function () {
                single_answer.classList.remove("input_field_shake");
            }, shake_duration);
            shake = true;
        }
    });

    // reset images and set red and green text
    if (!shake) {
        let counter = 0;
        answer_divs.forEach(function (single_answer) {
            if (single_answer.innerHTML.includes('<img')) {
                let imgElement = single_answer.querySelector('img');
                let imgID = imgElement.getAttribute('id');

                task_pics.append(imgElement);
                task_pics.querySelector('.img_placeholder').remove();

                let kids_answer = single_answer.innerText = imgID;
                if (kids_answer === solution[counter]) {
                    single_answer.style.color = 'green';
                } else {
                    single_answer.style.color = 'red';
                }
            }
            counter += 1;
        });

        // correct red answers to green answers
        setTimeout(function () {
            let counter = 0;
            answer_divs.forEach(function (single_answer) {
                single_answer.innerHTML = solution[counter];
                single_answer.style.color = 'green';
                counter += 1;
            })
        }, red_to_green_duration);

        // submit form
        setTimeout(function () {
            document.getElementById("example_form").submit();
        }, wrong_forward);
    }
    return false;
}

_scree