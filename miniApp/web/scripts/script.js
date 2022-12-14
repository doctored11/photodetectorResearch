let inputs = document.querySelectorAll('.form__input');
let inputBoxes = document.querySelectorAll('.form__input-box');
// let list;

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
      unBlock('blocked-choice');
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
          checkArray[14].value == '' &&
          checkArray[12].value == ''
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
      : (p.textContent = '' + array[i]);

    consoleBlock.append(p);
  }
}

eel.expose(clearAll);
function clearAll() {
  let simpleBarContent = document.querySelector('.simplebar-content');

  let consoleBlock = document.querySelector('.left-menu__content-part');
  if (simpleBarContent) consoleBlock = simpleBarContent;
  consoleBlock.innerHTML = '';
  let outputBl = document.querySelector('.general-parameters__data');
  outputBl.innerHTML = '';
}

async function setToPython(x) {
  await eel.callFromJstoPy(x);
}

eel.expose(getFromPython);
function getFromPython(picture, className) {
  let img = document.querySelector(`.${className}`);
  console.log(img, `../${picture}`);
  img.src = `../sourse/${picture}`;
}

eel.expose(getGraph);
function getGraph(picture, className, id) {
  let infoBlock = document.querySelector('.info');

  let infoCard = document.createElement('div');
  infoCard.classList.add('info__card', 'info-card');
  infoBlock.append(infoCard);

  let imgBlock = document.createElement('div');
  imgBlock.classList.add('info__img');
  infoCard.append(imgBlock);
  // img
  let img = document.createElement('img');
  img.classList.add(`${className}`);
  img.src = `../sourse/${picture}`;
  imgBlock.append(img);

  let contentBlock = document.createElement('div');
  contentBlock.classList.add('info__content');
  infoCard.append(contentBlock);

  let propertyArr = [
    'id',
    'name_',
    'type',
    'num-el',
    'size',
    'd-lam',
    'Ur',
    'Rt',
    'It',
    'Icommon',
    'E',
    'Sva',
    'Svfk',
    'Sva-units',
    'Svfk-units',
    'Pmax',
    'mass',
    'Afcha',
    'tc',
  ];
  for (let i = 0; i < propertyArr.length; ++i) {
    let p = document.createElement('p');
    p.classList.add('info__property');
    p.textContent = propertyArr[i] + ' :  ' + list['info'][id - 1][propertyArr[i]];
    contentBlock.append(p);
  }
  addAniLoad();
}

//
eel.expose(getMultiplyGraph);
function getMultiplyGraph(picture, className, id) {
  let calcBlock = document.querySelector('.calc');
  let calcCard, resultBlock;
  let check = false;

  if (!document.querySelector(`.calc-${id}`)) {
    calcCard = document.createElement('div');
    calcCard.classList.add('calc__card', 'calc-card', `calc-${id}`);
    calcBlock.append(calcCard);
    addAniLoad();
  } else {
    calcCard = document.querySelector(`.calc-${id}`);
    if (!document.querySelector(`.calc__block-${id}`)) {
      resultBlock = document.createElement('div');
      resultBlock.classList.add(`calc__block-${id}`);
      check = true;
    }
  }

  let imgBlock = document.createElement('div');
  imgBlock.classList.add('info__img');
  calcCard.append(imgBlock);
  if (check) calcCard.append(resultBlock); //
  // img
  let img = document.createElement('img');
  img.classList.add(`${className}`);
  img.src = `../sourse/${picture}`;
  imgBlock.append(img);

  giveClickImg();
}
//

eel.expose(getUnblock);
function getUnblock() {
  setTimeout(() => {
    unBlock('active-ani');
  }, 3500);
}

eel.expose(getCalcResult);
function getCalcResult(id, resArr) {
  let resBlock = document.querySelector(`.calc__block-${id}`);

  for (let i = 0; i < resArr.length; ++i) {
    let p = document.createElement('p');
    if (resArr[i][1].includes('e')) {
      let buff = resArr[i][1].split('e');
      p.innerHTML =
        resArr[i][0] + ' ' + buff[0] + '<span class="accent"> * 10^ </span>' + buff[1];
    } else {
      p.textContent = resArr[i][0] + ' ' + resArr[i][1];
    }
    resBlock.append(p);
  }

  giveClickImg();
}

document.addEventListener('DOMContentLoaded', () => {
  blockSelectSection();
  let plusBtn = document.querySelector('.plus-btn');
  plusBtn.addEventListener('click', addInputCard);

  let autoBtn = document.querySelector('.auto-btn');
  autoBtn.addEventListener('click', startAutoCalc);

  let btns = document.querySelectorAll('.btn');
  console.log('загрузка');
  for (let i = 0; i < btns.length; ++i) {
    btns[i].addEventListener('click', giveClickImg);
    btns[i].addEventListener('click', clearGraph);
  }
});
async function getJS() {
  await eel.callJson();
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
eel.expose(getJson);
function getJson(text) {
  console.log(text);
}
function clearGraph() {
  console.log('clearClick');
  let inf = document.querySelector('.info');
  let cal = document.querySelector('.calc');
  inf.innerHTML = '  ';
  cal.innerHTML = '  ';
}

function giveClickImg() {
  let imgs = document.querySelectorAll('img');
  console.log(imgs);
  for (let i = 0; i < imgs.length; ++i) {
    imgs[i].addEventListener('click', () => {
      zoomImg(imgs[i].src);
    });
  }
}

function zoomImg(url) {
  if (document.querySelector('.back')) return;
  let back = document.createElement('div');
  back.classList.add('back');
  document.body.append(back);

  document.body.classList.add('reserved');

  let card = document.createElement('div');
  card.classList.add('zoom-card');
  back.append(card);

  let img = document.createElement('img');
  img.src = url;
  card.append(img);

  back.addEventListener('click', () => {
    back.remove();
    document.body.classList.remove('reserved');
  });
}

function blockSelectSection() {
  let block = document.createElement('div');
  block.classList.add('blocked', 'blocked-choice');

  let section = document.querySelector('.choice');

  section.append(block);
}

function unBlock(className) {
  let forDel = document.querySelectorAll(`.${className}`);
  for (let i = 0; i < forDel.length; ++i) {
    forDel[i].remove();
  }
}

function addAniLoad() {
  let textArr = [
    'Сейчас, уже рисую',
    'Еще пара штрихов',
    'Да груЖу я, гружу',
    'Считаем...',
    'Загрузка...',
    'Загрузка...',
    'Загрузка...',
    'Ну да, ручки из попы и что?',
    'Загрузка...',
    'Грузим...',
    'Сейчас сообразим',
    'Подгоняю результаты)',
  ];
  console.log('aniani');
  function create() {
    let aniBlock = document.createElement('div');
    aniBlock.classList.add('ani-block');

    let activeAni = document.createElement('div');
    activeAni.classList.add('active-ani');
    activeAni.append(aniBlock);

    let pencil = document.createElement('div');
    pencil.classList.add('pencil');
    aniBlock.append(pencil);

    let point = document.createElement('div');
    point.classList.add('pencil__ball-point');
    pencil.append(point);

    let cap = document.createElement('div');
    cap.classList.add('pencil__cap');
    pencil.append(cap);

    let base = document.createElement('div');
    base.classList.add('pencil__cap-base');
    pencil.append(base);

    let mid = document.createElement('div');
    mid.classList.add('pencil__middle');
    pencil.append(mid);

    let rub = document.createElement('div');
    rub.classList.add('pencil__eraser');
    pencil.append(rub);

    let line = document.createElement('div');
    line.classList.add('line');
    aniBlock.append(line);

    let text = document.createElement('h2');
    text.classList.add('load-txt');
    let rand = Math.floor(Math.random() * textArr.length);
    console.log(rand);
    text.textContent = textArr[rand];
    aniBlock.append(text);

    return activeAni;
  }

  let infCards = document.querySelectorAll('.info__card');
  let calcCards = document.querySelectorAll('.calc__card');

  for (let i = 0; i < infCards.length; ++i) {
    if (!infCards[i].querySelector('.active-ani')) {
      activeAni = create();
      infCards[i].append(activeAni);
    }
  }
  for (let i = 0; i < calcCards.length; ++i) {
    if (!calcCards[i].querySelector('.active-ani')) {
      activeAni = create();
      calcCards[i].append(activeAni);
    }
  }
}

// unBlock('active-ani');

function addInputCard() {
  let ulCards = document.querySelector('.choice__choice-cards-list');
  ulCards.innerHTML +=
    '<li class="choice__card"><form action="#" id="form" autocomplete="off" class="choice__form"><div class="choice__select"><select name="select" id="select" class="choice__list"><option value="">фотоприемник</option><option value="2">Имя</option><option value="3">Имя</option><option value="4">Имя</option></select></div><div class="choice__parameters parameters"></div></form></li>';
  getJS();
}

async function startAutoCalc() {
  await eel.autoCalcAll();
}
