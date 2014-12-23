// Insert code here to run when the DOM is ready
$(document).ready( function() {

	//var $deleteBtns = $('.delete-btn');
	var $itemList = $('#todo-list');
	$itemList.on('click', '.delete-btn', deleteItem);

	function deleteItem(e) {
		var id = $(this).attr('data-item-id');
		var csrf = $('input[name="csrfmiddlewaretoken"]').val();
		var $item = $(this);

		var deleteRequest = $.post(
			'/shared-todo-list/delete-item/' + id, 
			{ csrfmiddlewaretoken: csrf }
		);

		deleteRequest.done(function(data) {
			$item.parent().remove();
		});
	}

	var $form = $('form');
	$form.off();
	$form.on('click', 'input[type="submit"]', addItem);

	function addItem(e) {
		var csrf = $('input[name="csrfmiddlewaretoken"]').val();
		var inputText = $('input[name="item"]').val();
		var addRequest = $.post(
			'/shared-todo-list/add-item',
			{ 
				csrfmiddlewaretoken: csrf,
				item: inputText
			},
			function(data) {
				var lastItem = $(data)
									.filter('#todo-list')
									.children()
									.last();
				$itemList.append(lastItem);
			}
		);

		return false;
	}

});
