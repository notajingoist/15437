var GRUMBLR = {
	init: function() {
		this.$hiddenPhotoInput = $('#edit-upload-picture-hidden');
		this.bindEvents();
		// console.log("loaded javascript")
	},

	bindEvents: function() {
		// $('#btn-register').on('click', this.expandForm.bind(this, '#form-register'));
		// $('#btn-login').on('click', this.expandForm.bind(this, '#form-login'));
		// $('#btn-reset').on('click', this.expandForm.bind(this, '#form-reset'));
		$('#reset-text').on('mouseover', this.activateHover.bind(this));
		$('#reset-text').on('mouseout', this.deactivateHover.bind(this));
		// this.$hiddenPhotoInput.on('change', this.uploadInput.bind(this));
		// $('#edit-upload-picture').on('click', this.triggerHiddenPhotoInput.bind(this));
	},

	uploadInput: function(e) {
		var filepath = this.$hiddenPhotoInput.val();
		var filename = filepath.split("\\");
		filename = filename[filename.length-1];

		$('#upload-filename').html(filename);//.css('background', filename);

		var fReader = new FileReader();
		var file = this.$hiddenPhotoInput[0].files[0];
		fReader.readAsDataURL(file);
		var context = this;

		fReader.onloadend = function(event){
			var result = event.target.result;
			
			var imageType = 'image/*';
			var pdfType = 'application/pdf';
			var mswordType = 'application/msword';

			alert(result);

			if (file.type.match(imageType)) {
				$('#edit-picture').css('background', result);
			}
		}

		e.preventDefault();
	},

	triggerHiddenPhotoInput: function(e) {
		console.log('triggering');
		this.$hiddenPhotoInput.trigger('click');
	},

	activateHover: function(e) {
		$(e.currentTarget).addClass('hover-state')
	},

	deactivateHover: function(e) {
		$(e.currentTarget).removeClass('hover-state');
	},

	expandForm: function() {
		var formId = arguments[0];
		var e = arguments[1];
		var el = $(e.currentTarget);

		
		$('.buttons').addClass('hidden');

		setTimeout(function(){
			$(formId).removeClass('hidden');
		});

		console.log(formId);
		console.log(el);
	}
}

GRUMBLR.init();