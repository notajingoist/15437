var todoList = document.getElementById('todolist');
var addBtn = document.getElementById('addBtn');
var input = document.getElementById('textfield');
addBtn.addEventListener('click', addItem);


function addItem() {
	var item = document.createElement('li');
	console.log(input.getAttribute('value'));
	item.innerHTML = input.value;

	var deleteBtn = document.createElement('button');
	deleteBtn.innerHTML = 'Delete';
	deleteBtn.addEventListener('click', deleteItem);
	item.appendChild(deleteBtn);

	todoList.appendChild(item);
}

function deleteItem() {
	this.parentNode.remove();
}