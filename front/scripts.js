/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/imoveis';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      // Clear existing rows in the table except the header
      clearTable();

      data.imoveis.forEach(item => insertList(
        item.owner_name,
        item.bathrooms,
        item.bedrooms,
        item.accommodates,
        item.beds,
        item.availability_365,
        item.region,
        item.outcome
      ));
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para limpar a tabela antes de re-renderizar
  --------------------------------------------------------------------------------------
*/
const clearTable = () => {
  let table = document.getElementById('myTable');
  // Remove all rows except the header (index 0)
  while (table.rows.length > 1) {
    table.deleteRow(1);
  }
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList();


/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postItem = async (inputOwnerName, inputBathroom, inputBedroom,
                        inputAccom, inputBeds, inputAval, 
                        inputRegion) => {
    
  const formData = new FormData();   
  formData.append('owner_name', inputOwnerName);
  formData.append('bathrooms', inputBathroom);
  formData.append('bedrooms', inputBedroom);
  formData.append('accommodates', inputAccom);
  formData.append('beds', inputBeds);
  formData.append('availability_365', inputAval);
  formData.append('region', inputRegion);

  let url = 'http://127.0.0.1:5000/imovel';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertDeleteButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const nomeItem = div.getElementsByTagName('td')[0].innerHTML;
      if (confirm("Você tem certeza?")) {
        div.remove();
        deleteItem(nomeItem);
        alert("Removido!");
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  console.log(item);
  let url = 'http://127.0.0.1:5000/imovel?owner_name=' + item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com nome, quantidade e valor 
  --------------------------------------------------------------------------------------
*/
const newItem = async () => {
  let inputOwnerName = document.getElementById("newOwnerName").value;
  let inputBathroom = document.getElementById("newBath").value;
  let inputBedroom = document.getElementById("newBedroom").value;
  let inputAccom = document.getElementById("newAccom").value;
  let inputBeds = document.getElementById("newBeds").value;
  let inputAval = document.getElementById("newAval").value;
  let inputRegion = document.getElementById("newRegion").value;

  // Verifique se o nome do produto já existe antes de adicionar
  const checkUrl = `http://127.0.0.1:5000/imovel?owner_name=${inputOwnerName}`;
  
  try {
    const response = await fetch(checkUrl, {
      method: 'GET'
    });

    // Check if the response status is 404, which indicates no matching owner name found
    if (response.status === 404) {
      alert("O nome do proprietário não foi encontrado. Adicionando novo imóvel.");
      postItem(inputOwnerName, inputBathroom, inputBedroom, inputAccom, inputBeds, inputAval, inputRegion);
      alert("Item adicionado!");
      getList(); // Re-render list from backend
    } else if (response.ok) {
      const data = await response.json();

      if (data.imoveis && data.imoveis.some(item => item.owner_name === inputOwnerName)) {
        alert("O imóvel já está cadastrado.\nCadastre o imóvel com um nome diferente ou atualize o existente.");
      } else if (inputOwnerName === '') {
        alert("O nome do proprietário não pode ser vazio!");
      } else if (isNaN(inputBathroom) || isNaN(inputBedroom) || isNaN(inputAccom) || isNaN(inputBeds) || isNaN(inputAval)) {
        alert("Esse(s) campo(s) precisam ser números!");
      } else {
        postItem(inputOwnerName, inputBathroom, inputBedroom, inputAccom, inputBeds, inputAval, inputRegion);
        alert("Item adicionado!");
        getList(); // Re-render list from backend
      }
    } else {
      alert("Erro ao verificar o nome do proprietário.");
    }
  } catch (error) {
    console.error('Error:', error);
    alert("Erro ao comunicar com o servidor.");
  }
};


/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (nameOwner, bathrooms, bedrooms, accommodates, beds, availability_365, region, price) => {
  var item = [nameOwner, bathrooms, bedrooms, accommodates, beds, availability_365, region, price];
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cell = row.insertCell(i);
    cell.textContent = item[i];
  }

  var deleteCell = row.insertCell(-1);
  insertDeleteButton(deleteCell);

  document.getElementById("newOwnerName").value = "";
  document.getElementById("newBath").value = "";
  document.getElementById("newBedroom").value = "";
  document.getElementById("newAccom").value = "";
  document.getElementById("newBeds").value = "";
  document.getElementById("newAval").value = "";
  document.getElementById("newRegion").value = "";

  removeElement();
}
