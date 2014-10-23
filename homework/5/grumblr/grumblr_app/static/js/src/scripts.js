var GRUMBLR = {
	init: function() {
		// this.$hiddenPhotoInput = $('#edit-upload-picture-hidden');
		this.setVars();
		this.bindEvents();
		// console.log("loaded javascript")
	},

	setVars: function() {
		this.$resetText = $('#reset-text');
		this.$addCommentBtns = $('.add-comment-btn');
		this.$addCommentBoxes = $('.add-comment-boxes');
		this.$showCommentsBtns = $('.show-comments-btn');
	},

	bindEvents: function() {
		// $('#btn-register').on('click', this.expandForm.bind(this, '#form-register'));
		// $('#btn-login').on('click', this.expandForm.bind(this, '#form-login'));
		// $('#btn-reset').on('click', this.expandForm.bind(this, '#form-reset'));
		this.$resetText.on('mouseover', this.activateHover.bind(this));
		this.$resetText.on('mouseout', this.deactivateHover.bind(this));

		this.$addCommentBtns.on('click',this.toggleAddCommentBox.bind(this));
		this.$showCommentsBtns.on('click', this.toggleComments.bind(this));
		// this.$hiddenPhotoInput.on('change', this.uploadInput.bind(this));
		// $('#edit-upload-picture').on('click', this.triggerHiddenPhotoInput.bind(this));
	},

	toggleAddCommentBox: function(e) {
		var $this = $(e.currentTarget);
		var postId = $this.data('postId');
		var $commentBox = $('#comment-box-' + postId);
		$commentBox.toggleClass('collapsed');

	},

	toggleComments: function(e) {
		var $this = $(e.currentTarget);
		var postId = $this.data('postId');
		var $comments = $('#comments-' + postId);
		$comments.stop(true, false).slideToggle(function() {
			$comments.toggleClass('collapsed');
		});
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