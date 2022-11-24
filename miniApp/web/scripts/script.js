let inputs = document.querySelectorAll('.form__input');
let inputBoxes = document.querySelectorAll('.form__input-box');
for (let i = 0; i < inputs.length; ++i) {
  inputs[i].oninput = function () {
    inputs[i].value
      ? inputBoxes[i].classList.add('active')
      : inputBoxes[i].classList.remove('active');
  };
}

let calcBtn = document.getElementById('start-calc-btn');
calcBtn.addEventListener('click', () => {
  clearAll();
  let arrayOfInputs = getInputValues();
  let errorsId = checkInputsEmpty(arrayOfInputs);
  console.log(errorsId);

  if (arrayOfInputs.length > 2) {
    if (errorsId.length < 1) {
      if (arrayOfInputs[13].value == '') arrayOfInputs[13].value = 2850;

      setToPython(arrayOfInputs);
    } else {
      consoleLog(errorsId, 'error');
    }
  } else {
    consoleLog(arrayOfInputs, 'error');
  }
});

function getInputValues() {
  let inputArray = [];
  let errorValid = [];
  inputArray = document.querySelectorAll('.form__input');

  let valueArray = [];

  for (i = 0; i < inputArray.length; ++i) {
    valueArray.push({
      id: inputArray[i].id,
      value: inputArray[i].value,
    });

    if (validateLineFloat(valueArray[i].value) == 1) {
      errorValid.push(valueArray[i].id + ' - неверное значение: ' + valueArray[i].value);
      return errorValid;
    }
  }
  return valueArray;
}

function validateLineFloat(line) {
  let array = [];
  numPoints = 0;
  let alfabet = '1234567890.';
  for (j = 0; j < line.length; ++j) {
    if (line[j] == '.') numPoints++;
    if (alfabet.includes(line[j]) && numPoints < 2) {
      console.log('');
    } else {
      return 1;
    }
  }
}

function checkInputsEmpty(checkArray) {
  let mandatory = ['lam', 'dFi', 'Rf', 'Fef', 'Tf', 'D', 'k']; //'Rl' - убрал
  let errorAr = [];
  console.log(checkArray);
  for (n = 0; n < checkArray.length; ++n) {
    for (i = 0; i < mandatory.length; ++i) {
      if (checkArray[n].id == mandatory[i] && checkArray[n].value == '')
        errorAr.push(mandatory[i]);
    }
    if (n > 0 && n < checkArray.length - 1) {
      if (checkArray[n + 1].id == 'fTop') {
        if (
          // молимся что порядок свойств не поменяется
          checkArray[n + 1].value == '' &&
          checkArray[14].value == '' && checkArray[12].value == ''
        ) {
          checkArray[14].value == '' ? errorAr.push('df') : errorAr.push('fTop');
        }
      }
      if (
        checkArray[n].id == 'Fel' &&
        checkArray[n].value == '' &&
        checkArray[n + 1].value == ''
      ) {
        checkArray[n + 1].value == '' ? errorAr.push('Wel') : errorAr.push('Fel');
      }
      if (checkArray[n].id == 'tImp') {
        if (checkArray[n].value == '' && checkArray[5].value != '') {
          errorAr.push('tImp');
        }
      }
    }
  }

  return errorAr;
}
eel.expose(consoleLog);
function consoleLog(array, className) {
  let consoleBlock = document.querySelector('.left-menu__content-part');

  let simpleBarContent = document.querySelector('.simplebar-content');
  if (simpleBarContent) consoleBlock = simpleBarContent;
  for (let i = 0, n = array.length; i < n; ++i) {
    let p = document.createElement('p');
    p.classList.add('context-p');
    p.classList.add(className);
    className == 'error'
      ? (p.textContent = '!ошибка значения: ' + array[i])
      : (p.textContent = array[i]);

    consoleBlock.append(p);
  }
}
function clearAll() {
  let simpleBarContent = document.querySelector('.simplebar-content');

  let consoleBlock = document.querySelector('.left-menu__content-part');
  if (simpleBarContent) consoleBlock = simpleBarContent;
  consoleBlock.innerHTML = '';
  let outputBl = document.querySelector('.general-parameters__data');
  outputBl.innerHTML = '';
}

// python
async function setToPython(x) {
  await eel.callFromJstoPy(x);
}

eel.expose(getFromPython);
function getFromPython(picture, className) {
  let img = document.querySelector(`.${className}`);
  console.log(img, `../${picture}`);
  img.src = `../sourse/${picture}`;
}

eel.expose(getResultsStep1);
function getResultsStep1(array) {
  console.log(array);
  let outputBox = document.querySelector('.general-parameters__data');
  outputBox.innerHTML = ' ';
  console.log(outputBox);

  for (let i = 0; i < array.length; ++i) {
    let p = document.createElement('p');
    p.classList.add('output-data__calculated-data', 'small-descr');

    p.textContent = array[i];
    outputBox.appendChild(p);
  }
}
