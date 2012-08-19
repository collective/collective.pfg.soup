if (typeof(window['PFGSOUP']) == "undefined") PFGSOUP = {};

$.extend(PFGSOUP, {
	asInitVals: new Array(),
	post: function(data, textStatus, jqXHR) {
		alert(data);
		var form = $('<form></form>');
		var path = $('#pfgsoupdata').attr('data-formurl');

	    form.attr("method", "post");
	    form.attr("action", path);

	    $.each(data, function(key, value) {
	        var field = $('<input type="hidden"></input>');
	        field.attr("name", key);
	        field.attr("value", value);

	        form.append(field);
	    });

	    // The form needs to be apart of the document in
	    // order for us to be able to submit it.
	    $(document.body).append(form);
	    form.submit();
	}
});

(function($) {
	$(document).ready(function() {
		var url = $('#pfgsoupdata').attr('data-ajaxurl');
		var oTable = $('#pfgsoupdata').dataTable( {
			"bProcessing": true,
			"bServerSide": true,
			"sAjaxSource": url,
			"sPaginationType": "full_numbers",
			'fnDrawCallback' : function(oSettings) {
				$("#pfgsoupdata tbody a.pfgsoup-edit").click(function() {
					var iid = $(this).attr('data-iid');
					var url = $('#pfgsoupdata').attr('data-editurl');
					$.ajax({
						  url: url,
						  dataType: 'json',
						  data: {iid : iid},
						  success: PFGSOUP.post
					});
			    });
			},
			"oLanguage": {
				"sSearch": "Alles durchsuchen:"
			}		
		});
		$("#pfgsoupdata tfoot input").keyup( function () {
			/* Filter on the column (the index) of this element */
			oTable.fnFilter( this.value, $("#pfgsoupdata tfoot input").index(this) );
		} );		
		$("#pfgsoupdata tfoot input").each( function (i) {
			PFGSOUP.asInitVals[i] = this.value;
		} );
		
		$("#pfgsoupdata tfoot input").focus( function () {
			if ( this.className == "search_init" )
			{
				this.className = "";
				this.value = "";
			}
		} );		
		$("#pfgsoupdata tfoot input").blur( function (i) {
			if ( this.value == "" )
			{
				this.className = "search_init";
				this.value = PFGSOUP.asInitVals[$("#pfgsoupdata tfoot input").index(this)];
			}
		} );		
	});
})(jQuery);