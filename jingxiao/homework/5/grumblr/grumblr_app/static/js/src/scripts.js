var GRUMBLR = {
	init: function() {
		this.setVars();
		this.bindEvents();
		this.fetchComments();
		this.pollForPosts();
	},

	setVars: function() {
		this.$resetText = $('#reset-text');
		this.$addCommentBtns = $('.add-comment-btn');
		this.$addCommentBoxes = $('.add-comment-boxes');
		this.$showCommentsBtns = $('.show-comments-btn');
		this.$commentForms = $('.comment-form');
		this.$comments = $('.comments');
		this.$posts = $('.posts');

		this.pollingInterval = 10000;
	},

	bindEvents: function() {
		this.$resetText.on('mouseover', this.activateHover.bind(this));
		this.$resetText.on('mouseout', this.deactivateHover.bind(this));

		this.$addCommentBtns.on('click', this.toggleAddCommentBox.bind(this));
		this.$showCommentsBtns.on('click', this.toggleComments.bind(this));
		this.$commentForms.on('click', '.post-comment-btn', this.postComment.bind(this));
	},

	pollForPosts: function() {
		var context = this;
		console.log('would be polling...');
		var currentPath = window.location.pathname;
		var $allPosts = this.$posts.find('.post');
		var $latestPost = $allPosts.eq(0);
		var lastUpdate = $allPosts.length > 0 ? $latestPost.data('timestamp') : '';
		console.log("most recent post timestamp: " + lastUpdate);

		var postsRequest = $.get(
			'/fetch-posts/',
			{
				current_path: currentPath,
				last_update: lastUpdate
			},
			'json'
		);

		postsRequest.done(function(response) {
			//console.log("response..." + response);
		});

		setTimeout(function() {
			context.pollForPosts();
		}, this.pollingInterval);
	},

	fetchComments: function() {
		var context = this;
		this.$comments.each(function(idx, elem) {
			var $elem = $(elem);
			var postId = $elem.data('postId');

			var fetchCommentRequest = $.get(
				'/fetch-comments/',
				{
					post_id: postId
				},
				'json'
			);

			fetchCommentRequest.done(function(response) {
				$elem.html('');

				for (var i = 0; i < response.length; i++) {
					var comment = response[i].fields;
					var commentContent = comment.text;
					var commentPostId = comment.post;
					var commentAuthor = ''

					var getUserRequest = context.getUser(comment.user);

					getUserRequest.done(function(response) {
						for (var i = 0; i < response.length; i++) {
							commentAuthor = response[i].fields.username;
						}

						var commentHtml = '<div class="panel panel-default panel-grumblr panel-grumbl grumbl-text comment-post">' 
											+ commentContent 
											+ '<span class="post-info">Posted by <span class="author"><a href="/profile/' 
											+ commentAuthor + '">' 
											+ commentAuthor + '</a></span></span></div>';
						$elem.append(commentHtml);

					});
				}

				$('#comment-count-' + postId).html(response.length);
			});
		});



	},

	getUser: function(userId) {
		var getUserRequest = $.get('/get-user', { user_id: userId },'json');
		return getUserRequest;
	},

	toggleAddCommentBox: function(e) {
		var $this = $(e.currentTarget);
		var postId = $this.data('postId');
		var $commentBox = $('#comment-box-' + postId);
		var $errorPanel = $('#error-panel-' + postId);
		$commentBox.stop(true, false).slideToggle(function() {
			$commentBox.toggleClass('collapsed');
			$errorPanel.remove();
		});

		e.preventDefault();
	},

	toggleComments: function(e) {
		var $this = $(e.currentTarget);
		var postId = $this.data('postId');
		var $comments = $('#comments-' + postId);
		if ($comments.children().length > 0) {
			$comments.stop(true, false).slideToggle(function() {
				$comments.toggleClass('collapsed');
			});
		}
	
		e.preventDefault();
	},

	postComment: function(e) {
		var $this = $(e.currentTarget);
		var $form = $this.parent();
		var postId = $form.data('postId');
		var csrf = $form.find('input[name="csrfmiddlewaretoken"]').val();

		var $errorPanel = $('#error-panel-' + postId);
		$errorPanel.remove();
		var $comments = $('#comments-' + postId);
		var $commentBox = $('#comment-box-' + postId);
		var commentText = $form.find('.textarea-comment').val();
		var commentData = $form.data();
		var url = '/' + commentData.urlName + '/' 
					+ commentData.redirectName + '/' 
					+ commentData.userId + '/' 
					+ commentData.postId + '/';

		var postCommentRequest = $.post(
			url,
			{
				csrfmiddlewaretoken: csrf,
				text: commentText
			},
			'json'
		);

		var context = this;

		postCommentRequest.done(function(response) {
			console.log(response);

			if (response.length > 0 && response[0].errors) {
				console.log(response[1]);
				if (response.length > 1) {
					var errorPanel = '<div id="error-panel-' + postId + '"></div>'
					var $errorPanel = $(errorPanel).prependTo($commentBox);
					for (var i = 1; i < response.length; i++) {
						var errorMessage = response[i].text;
						var error = '<div class="panel panel-default panel-grumblr panel-message">'
											+ '<span class="glyphicon glyphicon-exclamation-sign"></span>'
											+ '<span class="panel-error-message">' 
											+ errorMessage + '</span></div>';
						$errorPanel.append(error);
					}
					console.log($errorPanel);
				}
						
			} else {
				for (var i = 0; i < response.length; i++) {

					var comment = response[i].fields;
					var commentContent = comment.text;
					var commentAuthor = ''
					var commentPostId = comment.post;

					var commentAuthor = ''

					var getUserRequest = context.getUser(comment.user);

					getUserRequest.done(function(response) {
						for (var i = 0; i < response.length; i++) {
							console.log(response[i]);
							commentAuthor = response[i].fields.username;
							console.log(commentAuthor);
						}

						var commentHtml = '<div class="panel panel-default panel-grumblr panel-grumbl grumbl-text comment-post">' + commentContent + '<span class="post-info">Posted by <span class="author"><a href="/profile/' + commentAuthor + '">' + commentAuthor + '</a></span></span></div>';
						$comments.append(commentHtml);

						var oldCount = $('#comment-count-' + postId).html();
						$('#comment-count-' + postId).html(parseInt(oldCount) + 1);

					});
				}
			}

			

			$form[0].reset();
		});

		postCommentRequest.fail(function(response) {
			console.log(response);
		});

		e.preventDefault();
	},

	activateHover: function(e) {
		$(e.currentTarget).addClass('hover-state')
	},

	deactivateHover: function(e) {
		$(e.currentTarget).removeClass('hover-state');
	},
}

GRUMBLR.init();