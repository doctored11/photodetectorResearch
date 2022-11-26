let list;

document.addEventListener('DOMContentLoaded', () => {
  getJS();
  eel.expose(getJson);
  function getJson(text) {
    console.log(text);
    list = text;
    addSelects();
  }
});
async function getJS() {
  await eel.callJson();
}

function addSelects() {
  let selects = document.querySelectorAll('.choice__list');
  console.log(selects);
  for (let i = 0; i < selects.length; ++i) {
    addOptions(selects[i]);
  }
}

function addOptions(item) {
  item.addEventListener('change', showPropertyes);
  item.innerHTML = '';

  for (let i = 0; i < list['info'].length; ++i) {
    let opt = document.createElement('option');
    opt.value = '' + i;
    opt.textContent = list['info'][i]['name_'];
    item.appendChild(opt);
  }
}
function showPropertyes() {
  console.log(this);
  let form = this.parentElement.parentElement;
  console.log(form);
  let txtBlock = form.querySelector('.parameters');
  console.log(txtBlock);
  txtBlock.innerHTML = '';
  console.log(list['info']);
  for (let i = 0; i < 6; ++i) {
    let paragraph = document.createElement('p');
    // console.log('имя: ');
    paragraph.classList.add('parametrs-parametr');
    switch (i) {
      case 0:
        paragraph.textContent = 'имя: ' + list['info'][this.value]['name_'];
        break;
      case 1:
        paragraph.textContent = 'тип: ' + list['info'][this.value]['type'];
        break;
      case 2:
        paragraph.textContent = 'длина волны: ' + list['info'][this.value]['d-lam'];
        break;
      case 3:
        paragraph.textContent = 'темновой ток: ' + list['info'][this.value]['It'];
        break;
      case 4:
        paragraph.textContent =
          'Sva: ' +
          list['info'][this.value]['Sva'] +
          ' ' +
          list['info'][this.value]['Sva-units'];
        break;
      case 5:
        paragraph.textContent =
          'Svfk: ' +
          list['info'][this.value]['Svfk'] +
          ' ' +
          list['info'][this.value]['Svfk-units'];
        break;
    }

    txtBlock.appendChild(paragraph);
  }
}
