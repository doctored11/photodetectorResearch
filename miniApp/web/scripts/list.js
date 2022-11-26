let list;
const table = document.querySelector('.table__body');
document.addEventListener('DOMContentLoaded', () => {
  getJS();
  eel.expose(getJson);
  function getJson(text) {
    console.log(text);
    list = text;
    buf();
  }
});

async function getJS() {
  await eel.callJson();
}

function buf() {
  console.log(list);
  console.log(list['info']);
  for (let i = 0; i < list['info'].length; ++i) {
    createTAble(i);
  }
}

function createTAble(id) {
  let tr = document.createElement('tr');
  for (let i = 0; i < 4; ++i) {
    let td = document.createElement('td');
    td.classList.add('table__cell');
    switch (i) {
      case 0:
        td.textContent = list['info'][id]['id'];
        break;
      case 1:
        td.textContent = list['info'][id]['name_'];
        break;
      case 2:
        td.textContent = list['info'][id]['d-lam'];
        break;
      case 3:
        td.innerHTML = `<a class = "table__link" target = "_blank" href = "${list['info'][id]['link']}">глянуть</a>`;

        break;
      default:
        td.textContent = '-';
        break;
    }
    tr.appendChild(td);
  }
  table.appendChild(tr);
}
