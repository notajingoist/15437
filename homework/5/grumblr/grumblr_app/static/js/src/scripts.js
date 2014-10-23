var GRUMBLR = {
	init: function() {
		// this.$hiddenPhotoInput = $('#edit-upload-picture-hidden');
		this.setVars();
		this.bindEvents();

		this.fetchComments();
		// console.log("loaded javascript")
	},

	setVars: function() {
		this.$resetText = $('#reset-text');
		this.$addCommentBtns = $('.add-comment-btn');
		this.$addCommentBoxes = $('.add-comment-boxes');
		this.$showCommentsBtns = $('.show-comments-btn');
		// this.$postCommentBtns = $('.post-comment-btn');
		this.$commentForms = $('.comment-form');
		this.$comments = $('.comments');
	},

	bindEvents: function() {
		// $('#btn-register').on('click', this.expandForm.bind(this, '#form-register'));
		// $('#btn-login').on('click', this.expandForm.bind(this, '#form-login'));
		// $('#btn-reset').on('click', this.expandForm.bind(this, '#form-reset'));
		this.$resetText.on('mouseover', this.activateHover.bind(this));
		this.$resetText.on('mouseout', this.deactivateHover.bind(this));

		this.$addCommentBtns.on('click', this.toggleAddCommentBox.bind(this));
		this.$showCommentsBtns.on('click', this.toggleComments.bind(this));
		this.$commentForms.on('click', '.post-comment-btn', this.postComment.bind(this));
		// this.$hiddenPhotoInput.on('change', this.uploadInput.bind(this));
		// $('#edit-upload-picture').on('click', this.triggerHiddenPhotoInput.bind(this));
	},

	fetchComments: function() {
		var context = this;
		this.$comments.each(function(idx, elem) {
			var $elem = $(elem);
			var postId = $elem.data('postId');



			var fetchCommentRequest = $.get(
				'/fetch-comments',
				{
					post_id: postId
				},
				'json'
			);

			fetchCommentRequest.done(function(response) {
				$elem.html('');

				for (var i = 0; i < response.length; i++) {



					console.log(response[i]);
					var comment = response[i].fields;
					var commentContent = comment.text;
					var commentPostId = comment.post;
					// var commentUserId = comment.user;
					var commentAuthor = ''

					var getUserRequest = context.getUser(comment.user);

					getUserRequest.done(function(response) {
						for (var i = 0; i < response.length; i++) {
							console.log(response[i]);
							commentAuthor = response[i].fields.username;
							console.log(commentAuthor);
						}

						var commentHtml = '<div class="panel panel-default panel-grumblr panel-grumbl grumbl-text comment-post">' 
											+ commentContent 
											+ '<span class="post-info">Posted by <span class="author"><a href="/profile/' 
											+ commentAuthor + '">' 
											+ commentAuthor + '</a></span></span></div>';
						$elem.append(commentHtml);

					});

					// commentAuthor.done(function(response) {
					// 	console.log(response.length);
					// 	for (var i = 0; i < response.length; i++) {
					// 		console.log(response[i]);
					// 		username = response[i].fields.username;
					// 	}
					// 	console.log(response);
					// });


					// var commentAuthor = 'notajingoist';//context.getUser(comment.user);//comment.user;
					
					// var commentHtml = '<div class="panel panel-default panel-grumblr panel-grumbl grumbl-text comment-post">' 
					// 					+ commentContent 
					// 					+ '<span class="post-info">Posted by <span class="author"><a href="/profile/"' 
					// 					+ commentAuthor + '">' 
					// 					+ commentAuthor + '</a></span></span></div>';
					// $elem.append(commentHtml);
				}

				$('#comment-count-' + postId).html(response.length);
			});
		});



	},

	getUser: function(userId) {
		var getUserRequest = $.get(
			'/get-user',
			{
				user_id: userId
			},
			'json'
		);

		var context = this;
		//var username = '';

		//$deferred = new $.Deferred();

		// getUserRequest.done(function(response) {
		// 	for (var i = 0; i < response.length; i++) {
		// 		console.log(response[i]);
		// 		var username = response[i].fields.username;
		// 	}
		// 	//return username
		// 	//console.log(username);
		// });

		//return $deferred.promise();
		return getUserRequest;
	},

	toggleAddCommentBox: function(e) {
		var $this = $(e.currentTarget);
		var postId = $this.data('postId');
		var $commentBox = $('#comment-box-' + postId);
		$commentBox.stop(true, false).slideToggle(function() {
			$commentBox.toggleClass('collapsed');
		});

		e.preventDefault();
	},

	toggleComments: function(e) {
		var $this = $(e.currentTarget);
		var postId = $this.data('postId');
		var $comments = $('#comments-' + postId);
		$comments.stop(true, false).slideToggle(function() {
			$comments.toggleClass('collapsed');
		});

		e.preventDefault();
	},

	postComment: function(e) {
		var $this = $(e.currentTarget);
		var $form = $this.parent();
		var postId = $form.data('postId');
		var csrf = $form.find('input[name="csrfmiddlewaretoken"]').val();

		var $comments = $('#comments-' + postId);
		console.log($comments);
		
		// var urlName = $form.data('urlName');
		// var redirectName = $form.data('redirectName');
		// var userId = $form.data('userId');
		// var postId = $form.data('postId');
		
		var commentText = $form.find('.textarea-comment').val();

		var commentData = $form.data();
		var url = commentData.urlName + '/' 
					+ commentData.redirectName + '/' 
					+ commentData.userId + '/' 
					+ commentData.postId;
					
		//var url = '/post-comment';

		var postCommentRequest = $.post(
			url,
			{
				csrfmiddlewaretoken: csrf,
				text: commentText
			},
			'json'
		);

		postCommentRequest.done(function(response) {
			//console.log(jQuery.parseJSON('[{"blah": "blah"}]'));
			
			// $comments.html('');

			for (var i = 0; i < response.length; i++) {
				var comment = response[i].fields;
				var commentContent = comment.text;
				var commentAuthor = comment.user;
				var commentPostId = comment.post;
				//console.log(commentContent);


				var commentHtml = '<div class="panel panel-default panel-grumblr panel-grumbl grumbl-text comment-post">' + commentContent + '<span class="post-info">Posted by <span class="author"><a href="/profile/"' + commentAuthor + '">' + commentAuthor + '</a></span></span></div>';
				$comments.append(commentHtml);

				var oldCount = $('#comment-count-' + postId).html();
				$('#comment-count-' + postId).html(parseInt(oldCount) + 1);

				//$comments.append($(commentHtml));
			}

			$form[0].reset();

		});

		e.preventDefault();
		//return false;
	},

	// uploadInput: function(e) {
	// 	var filepath = this.$hiddenPhotoInput.val();
	// 	var filename = filepath.split("\\");
	// 	filename = filename[filename.length-1];

	// 	$('#upload-filename').html(filename);//.css('background', filename);

	// 	var fReader = new FileReader();
	// 	var file = this.$hiddenPhotoInput[0].files[0];
	// 	fReader.readAsDataURL(file);
	// 	var context = this;

	// 	fReader.onloadend = function(event){
	// 		var result = event.target.result;
			
	// 		var imageType = 'image/*';
	// 		var pdfType = 'application/pdf';
	// 		var mswordType = 'application/msword';

	// 		alert(result);

	// 		if (file.type.match(imageType)) {
	// 			$('#edit-picture').css('background', result);
	// 		}
	// 	}

	// 	e.preventDefault();
	// },

	// triggerHiddenPhotoInput: function(e) {
	// 	console.log('triggering');
	// 	this.$hiddenPhotoInput.trigger('click');
	// },

	activateHover: function(e) {
		$(e.currentTarget).addClass('hover-state')
	},

	deactivateHover: function(e) {
		$(e.currentTarget).removeClass('hover-state');
	},

	// expandForm: function() {
	// 	var formId = arguments[0];
	// 	var e = arguments[1];
	// 	var el = $(e.currentTarget);

		
	// 	$('.buttons').addClass('hidden');

	// 	setTimeout(function(){
	// 		$(formId).removeClass('hidden');
	// 	});

	// 	console.log(formId);
	// 	console.log(el);
	// }
}

GRUMBLR.init();