document.addEventListener('DOMContentLoaded', () => {
  let calcBtn = document.getElementById('calc-btn');

  calcBtn.addEventListener('click', () => {
    console.log('_');
    let check = document.querySelectorAll('.choice__list');
    let arrayCheckPhoto = [];
    arrayCheckPhoto.push(Number(check[0].value) + 1);
    arrayCheckPhoto.push(Number(check[1].value) + 1);
    arrayCheckPhoto.push(Number(check[2].value) + 1);
    console.log(arrayCheckPhoto);
    pyCalc(arrayCheckPhoto);
  });
});

async function pyCalc(arr) {
  await eel.getArray3toCalc(arr);
}
