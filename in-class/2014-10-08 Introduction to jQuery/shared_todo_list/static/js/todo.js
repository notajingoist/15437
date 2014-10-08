// Insert code here to run when the DOM is ready
$(document).ready( function() {

	var $deleteBtns = $('.delete-btn');
	$deleteBtns.on('click', deleteItem);

	function deleteItem(e) {
		var id = $(this).attr('data-item-id');
		var csrf = $('input[name="csrfmiddlewaretoken"]').val();
		var $item = $(this);

		var deleteRequest = $.post(
			'/shared-todo-list/delete-item/' + id, 
			{ csrfmiddlewaretoken: csrf }
		);

		deleteRequest.done(function() {
			$item.parent().remove();
		});
	}

});
