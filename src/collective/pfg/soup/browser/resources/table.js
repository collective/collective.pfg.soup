(function($) {
	$(document).ready(function() {
		var url = $('#pfgsoupdata').attr('data-ajaxurl');
		$('#pfgsoupdata').dataTable( {
			"bProcessing": true,
			"bServerSide": true,
			"sAjaxSource": url
		});
	});
})(jQuery);