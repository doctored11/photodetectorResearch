document.addEventListener('DOMContentLoaded', () => {
  let calcBtn = document.getElementById('calc-btn');

  calcBtn.addEventListener('click', clickCalc);
});

function clickCalc() {
  console.log('_');
  let check = document.querySelectorAll('.choice__list');
  let arrayCheckPhoto = [];
  for (let i = 0; i < check.length; ++i) {
    arrayCheckPhoto.push(Number(check[i].value) + 1);
  }
  console.log(arrayCheckPhoto);
  pyCalc(arrayCheckPhoto);
}

async function pyCalc(arr) {
  await eel.getArray3toCalc(arr);
}
