var GRUMBLR = {
	init: function() {
		this.bindEvents();
	},

	bindEvents: function() {
		$('#btn-register').on('click', this.expandForm.bind(this, '#form-register'));
		$('#btn-login').on('click', this.expandForm.bind(this, '#form-login'));
		$('#btn-reset').on('click', this.expandForm.bind(this, '#form-reset'));
		$('#reset-text').on('mouseover', this.activateHover.bind(this));
		$('#reset-text').on('mouseout', this.deactivateHover.bind(this));
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